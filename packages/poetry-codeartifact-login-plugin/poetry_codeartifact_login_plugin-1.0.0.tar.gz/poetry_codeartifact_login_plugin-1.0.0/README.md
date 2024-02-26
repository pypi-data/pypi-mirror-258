# poetry-codeartifact-login-plugin

This is a plugin for [Poetry](https://python-poetry.org/) that allows poetry to obtain and use login credentials for 
an AWS CodeArtifact repository.

## Background

CodeArtifact is AWS's solution for hosting Python packages (and other languages). Users must authenticate with
CodeArtifact using http-basic authentication (anonymous access is not supported). Users can obtain the necessary
credentials by using the AWS CLI. A user who is properly authenticated with AWS can obtain a login token for
CodeArtifact that will expire after a certain amount of time (by default, 12 hours). This plugin allows Poetry to
automatically obtain and use these credentials.

## Dependencies

This plugin depends on the AWS CLI being installed on the search $PATH. The AWS CLI must be properly configured
with the necessary credentials and region. 

## Setup

Update your project's `pyproject.toml` file to include your CodeArtifact repository as a source for packages.
For example,

```toml
[[tool.poetry.source]]
name = "MyRepository"
url = "https://mydomain-1234567890123.d.codeartifact.us-west-2.amazonaws.com/pypi/my-repository/simple/"
default = true
```

Next, add a `[tool.poetry_codeartifact_login]` section to your `pyproject.toml` file. For each CodeArtifact
repository in your list of sources, add a corresponding `[[tool.poetry_codeartifact_login.source]]` section.
For example,

```toml
[tool.poetry_codeartifact_login]
[[tool.poetry_codeartifact_login.source]]
name = "MyRepository"
domain = "mydomain"
domain_owner = "1234567890123"
aws_profile = "developer-profile"
```

### Configuration
Each `[[tool.poetry_codeartifact_login.source]]` section has the following fields:

- `name`: This must match the name of the source as defined in the corresponding `[[tool.poetry.source]]` section.
- `domain`: The name of the domain of the CodeArtifact repository.
- `domain_owner`: The AWS account number that owns the domain.
- `aws_profile`: (OPTIONAL) The name of the AWS profile to use when obtaining credentials. If not provided,
  the default profile will be used.

## Usage
Once the plugin is installed, and a project configured with the necessary `pyproject.toml` settings, poetry will
automatically attempt to refresh the CodeArtifact login token before each operation that requires it. If
all works as expected, you should not need to do anything else.

## Architecture

The plugin registers a hook that runs prior to each operation that requires a login token. The hook checks if the
is valid, unexpired token is already available. If not, the plugin runs the `aws codeartifact get-authorization-token`
command to obtain a new token, and stores it in the poetry configuration for the corresponding repository.

The plugin uses the standard poetry functionality for storage and management of credentials. Poetry will
attempt to use a platform-specific keyring to store the credentials, if available. Otherwise, the credentials
will be stored in a poetry configuration flatfile on disk. Refer to the 
[poetry documentation](https://python-poetry.org/docs/repositories/#configuring-credentials) for more information.
