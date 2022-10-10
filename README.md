# ansible-generator

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Generate documentation and continuous integration files for an Ansible Role.

## Input

This script loads input from:

- meta/main.yml*
- meta/version.yml
- meta/exception.yml
- meta/preferences.yml
- defaults/main.yml
- requirements.yml
- molecule/default/prepare.yml
- molecule/default/converge.yml*
- molecule/default/verify.yml
- generate_modules.sh
- secure.yml
- Ansible Galaxy

(Items with a star are mandatory)

## Output

This script writes output to:

- README.md
- molecule/default/molecule.yml
- CONTRIBUTING.md
- SECURITY.md
- LICENSE
- .travis.yml
- tox.ini
- .ansible-lint*
- .github/workflows/ansible.yml
- .github/workflows/galaxy.yml
- .github/workflows/release_drafter.yml
- .github/dependabot.yml
- .github/release-drafter.yml

## Usage

```bash
cd ansible-role-my_role
../path/to/generate.yml
```

## Configuration

In `vars/main.yml` you can change these variable to customize the output.

```yaml
---
# Settings to Docker containers.
docker_namespace: buluma
docker_image: fedora
docker_tag: latest

# References to travis use a namespace, this is likely your username on Travis.
travis_namespace: buluma

# Documentation refers to Ansible Galaxy. this is likely your username on Galaxy.
galaxy_namespace: buluma

# Your username/organization name on GitHub.
github_namespace: buluma

# Your name and optionally email-address.
author: Michael Buluma (me@buluma.github.io)

# The full URL to your website.
author_website: "https://buluma.github.io/"
```

## meta/version.yml

This optional file can be placed when a role contains a version.

```yaml
---
project_name: Ansible
reference: "defaults/main.yml"
versions:
  - name: ansible
    url: "https://github.com/ansible/ansible/releases"
```

## meta/exception.yml

This optional file describes why some build are excepted.

```yaml
---
exceptions:
  - variation: alpine
    reason: "Not idempotent"
```

## meta/preferences.yml

This optional file describes how Travis, Tox and Molecule should behave.

|parameter       |type           |default|description|
|----------------|---------------|-------|-----------|
|tox_version     |list of strings|not set|What versions should Tox test? (Default: all.)|
|enterprise_linux|string         |not set|If `EL` is used in `meta/main.yml` where should tests happen on? (Default: `rockylinux`.)


```yaml
---
tox_versions:
  - current
enterprise_linx: centos
```
