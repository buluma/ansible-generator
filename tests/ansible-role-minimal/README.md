# [Ansible role minimal](#ansible-role-minimal)

Install and configure minimal on your system.

|GitHub|GitLab|Downloads|Version|
|------|------|---------|-------|
|[![github](https://github.com/buluma/ansible-role-minimal/workflows/Ansible%20Molecule/badge.svg)](https://github.com/buluma/ansible-role-minimal/actions)|[![gitlab](https://gitlab.com/shadowwalker/ansible-role-minimal/badges/master/pipeline.svg)](https://gitlab.com/shadowwalker/ansible-role-minimal)|[![downloads](https://img.shields.io/ansible/role/d/buluma/minimal)](https://galaxy.ansible.com/buluma/minimal)|[![Version](https://img.shields.io/github/release/buluma/ansible-role-minimal.svg)](https://github.com/buluma/ansible-role-minimal/releases/)|

## [Example Playbook](#example-playbook)

This example is taken from [`molecule/default/converge.yml`](https://github.com/buluma/ansible-role-minimal/blob/master/molecule/default/converge.yml) and is tested on each push, pull request and release.

```yaml
---
- name: Converge
  hosts: all
  become: yes
  gather_facts: yes

  roles:
    - role: ansible-role-minimal
```

Also see a [full explanation and example](https://buluma.github.io/how-to-use-these-roles.html) on how to use these roles.


## [Requirements](#requirements)

- pip packages listed in [requirements.txt](https://github.com/buluma/ansible-role-minimal/blob/master/requirements.txt).


## [Context](#context)

This role is part of many compatible roles. Have a look at [the documentation of these roles](https://buluma.github.io/) for further information.

Here is an overview of related roles:
![dependencies](https://raw.githubusercontent.com/buluma/ansible-role-minimal/png/requirements.png "Dependencies")

## [Compatibility](#compatibility)

This role has been tested on these [container images](https://hub.docker.com/u/buluma):

|container|tags|
|---------|----|
|[Alpine](https://hub.docker.com/r/buluma/alpine)|all|
|[Amazon](https://hub.docker.com/r/buluma/amazonlinux)|all|
|[Debian](https://hub.docker.com/r/buluma/debian)|all|
|[EL](https://hub.docker.com/r/buluma/enterpriselinux)|all|
|[Fedora](https://hub.docker.com/r/buluma/fedora)|all|
|[Ubuntu](https://hub.docker.com/r/buluma/ubuntu)|all|

The minimum version of Ansible required is 2.10, tests have been done on:

- The previous version.
- The current version.
- The development version.

If you find issues, please register them on [GitHub](https://github.com/buluma/ansible-role-minimal/issues).

## [License](#license)

[Apache-2.0](https://github.com/buluma/ansible-role-minimal/blob/master/LICENSE).

## [Author Information](#author-information)

[buluma](https://buluma.github.io/)
