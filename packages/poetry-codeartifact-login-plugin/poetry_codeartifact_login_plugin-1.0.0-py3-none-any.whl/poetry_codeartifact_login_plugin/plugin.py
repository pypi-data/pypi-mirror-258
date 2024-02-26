import os
from typing import Optional

from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.console.application import Application
from cleo.events.console_events import COMMAND
from cleo.events.event import Event
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.commands.env_command import EnvCommand
import subprocess
import logging
import json
from datetime import datetime, timedelta, timezone
from typing import Dict
from poetry.utils.password_manager import PasswordManager, PoetryKeyringError


class CodeArtifactLoginPlugin(ApplicationPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_by_source = None

    def activate(self, application: Application):
        super().activate(application=application)
        logger = logging.getLogger(__name__)

        logger.info("Activating CodeArtifactLoginPlugin")

        plugin_config = application.poetry.pyproject.data.get("tool", {}).get(
            "poetry_codeartifact_login", {}
        )

        poetry_sources = application.poetry.pyproject.poetry_config.get("source", [])
        poetry_sources_by_name = {source["name"]: source for source in poetry_sources}

        # Match each source defined in the plugin configuration (ie, a `[[tool.poetry_codeartifact_login.source]]`
        # block) with the corresponding source defined in the poetry configuration (ie, a `[[tool.poetry.source]]`
        # block).
        self._config_by_source = {}
        for source in plugin_config.get("source", []):
            name = source["name"]
            if name not in poetry_sources_by_name:
                logger.warning(
                    "CodeArtifactLogin source %s not found in poetry config", name
                )
                continue
            try:
                self._validate_config_source(source)
            except ValueError as e:
                logger.error(
                    "Error validating CodeArtifactLogin source config for source %s: %s",
                    name,
                    e,
                )
                continue

            self._config_by_source[name] = {
                "poetry_source_config": poetry_sources_by_name[name],
                "plugin_source_config": source,
            }

        application.event_dispatcher.add_listener(COMMAND, self.code_artifact_login)

    def code_artifact_login(
        self, event: Event, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        # This hook will run prior to each poetry command execution. We'll use it to refresh the CodeArtifact login
        # token if necessary.
        logger = logging.getLogger(__name__)

        if not isinstance(event, ConsoleCommandEvent):
            return
        command = event.command
        if not isinstance(command, EnvCommand):
            return

        # TODO: we can potentially filter out commands that won't talk to CodeArtifact and skip refreshing the token
        # in those cases.

        logger.info(
            "Refreshing CodeArtifact login in response to the %s command", command.name
        )

        password_manager = PasswordManager(command.poetry.config)
        auth_config_source = command.poetry.config.auth_config_source
        existing_credentials = command.poetry.config.all().get("http-basic", {})
        for source_name, source_config in self._config_by_source.items():
            if self._is_token_already_current(
                source_name, existing_credentials, password_manager
            ):
                logger.info(
                    "Auth token for source %s is still current, not refreshing",
                    source_name,
                )
                continue

            logger.info("Refreshing auth token for source %s", source_name)
            domain = source_config["plugin_source_config"]["domain"]
            domain_owner = source_config["plugin_source_config"]["domain_owner"]
            aws_profile = source_config["plugin_source_config"].get("aws_profile", None)

            try:
                auth_token = self._get_auth_token(domain, domain_owner, aws_profile)
            except Exception as e:
                logger.error(
                    "Error getting auth token for source %s: %s", source_name, e
                )
                continue

            logger.info("Got auth token for source %s", source_name)
            password_manager.set_http_password(
                source_name, "aws", auth_token["authorizationToken"]
            )
            auth_config_source.add_property(
                f"http-basic.{source_name}.expiration", auth_token["expiration"]
            )

    def _is_token_already_current(
        self, source_name: str, existing_credentials, password_manager: PasswordManager
    ):
        # Check if we have a credential already in the PasswordManager
        try:
            existing = password_manager.get_http_auth(source_name)
        except PoetryKeyringError:
            return False

        if not existing or not existing.get("password"):
            return False

        # If we have the credential in the PasswordManager, confirm that it is unexpired
        expiration = existing_credentials.get(source_name, {}).get("expiration", None)
        if expiration:
            expiration = datetime.fromisoformat(expiration)
            return expiration > datetime.now(timezone.utc) + timedelta(minutes=5)
        return False

    def _validate_config_source(self, source_config):
        # TODO: Can probably use a formal schema here with more specific errors
        if not all(
            source_config.get(key, None) is not None
            for key in ["name", "domain", "domain_owner"]
        ):
            raise ValueError(
                "source config must have name, domain, and domain_owner keys"
            )

    def _get_auth_token(
        self, domain: str, domain_owner: str, aws_profile: Optional[str]
    ) -> Dict[str, str]:
        env = dict(os.environ)
        if aws_profile:
            env["AWS_PROFILE"] = aws_profile
        token_info_string = (
            subprocess.check_output(
                [
                    "aws",
                    "codeartifact",
                    "get-authorization-token",
                    "--domain",
                    domain,
                    "--domain-owner",
                    domain_owner,
                ],
                env=env,
            )
            .decode("utf-8")
            .strip()
        )
        return json.loads(token_info_string)
