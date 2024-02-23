# cici-tools

<!-- BADGIE TIME -->

[![pipeline status](https://img.shields.io/gitlab/pipeline-status/buildgarden/tools/cici-tools?branch=main)](https://gitlab.com/buildgarden/tools/cici-tools/-/commits/main)
[![coverage report](https://img.shields.io/gitlab/pipeline-coverage/buildgarden/tools/cici-tools?branch=main)](https://gitlab.com/buildgarden/tools/cici-tools/-/commits/main)
[![latest release](https://img.shields.io/gitlab/v/release/buildgarden/tools/cici-tools)](https://gitlab.com/buildgarden/tools/cici-tools/-/releases)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![imports: isort](https://img.shields.io/badge/imports-isort-1674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-2a6db2)](https://mypy-lang.org/)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

<!-- END BADGIE TIME -->

> Do not use this software unless you are an active collaborator on the
> associated research project.
>
> This project is an output of an ongoing, active research project. It is
> published without warranty, is subject to change at any time, and has not been
> certified, tested, assessed, or otherwise assured of safety by any person or
> organization. Use at your own risk.

## Usage

### `bundle`

Flatten `extends` keywords to make zero-dependency GitLab CI/CD files.

```bash
cici bundle
```

```console
$ cici bundle
created python-autoflake.yml
created python-black.yml
created python-build-sdist.yml
created python-build-wheel.yml
created python-import-linter.yml
created python-isort.yml
created python-mypy.yml
created python-pyroma.yml
created python-pytest.yml
created python-setuptools-bdist-wheel.yml
created python-setuptools-sdist.yml
created python-twine-upload.yml
created python-vulture.yml
```

```yaml
include:
  - project: buildgarden/pipelines/python
    ref: ""
    file:
      - python-autoflake.yml
      - python-black.yml
      - python-isort.yml
```

### `fmt`

Normalize the style of your GitLab CI/CD files:

```bash
cici fmt
```

```console
$ cici fmt
.gitlab-ci.yml formatted
```

### `update`

Update to the latest GitLab CI/CD `include` versions available.

```bash
cici update
```

```console
$ cici update
updated buildgarden/pipelines/python to 0.5.1
updated buildgarden/pipelines/gitlab from 0.1.0 to 0.2.2
```
