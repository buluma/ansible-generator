# Project Overview

This project is an Ansible-based tool that generates documentation and continuous integration (CI) files for an Ansible Role. The primary goal is to automate the creation of boilerplate files, allowing developers to focus on the core logic of their Ansible roles.

The tool uses a main Ansible playbook, `generate.yml`, to read metadata and configuration from the target Ansible role, and then generates various files from templates.

## Building and Running

To use this tool, you need to have Ansible installed. The main execution is done through the `generate.yml` playbook.

**Running the generator:**

1.  Navigate to the directory of the Ansible role you want to process.
2.  Run the `generate.yml` playbook from the `ansible-generator` directory, pointing to the role's directory.

```bash
cd /path/to/your/ansible-role
/path/to/ansible-generator/generate.yml
```

**Configuration:**

The behavior of the generator can be customized by modifying the variables in `defaults/main.yml`. This file controls which files are generated, and allows for the configuration of Docker images, Galaxy and GitHub namespaces, and author information.

## Development Conventions

This project is an Ansible playbook and does not have traditional source code that requires compilation. The core logic is defined in YAML files within the project.

*   **Playbooks:** The main logic is in `generate.yml`.
*   **Templates:** All generated files are created from templates located in the `templates/` directory. These are Jinja2 templates.
*   **Default Variables:** Default configuration is stored in `defaults/main.yml`.
*   **Variables:** Additional variables are in `vars/main.yml`.
*   **Files:** Static files that are copied to the target role are located in the `files/` directory.
*   **Testing:** The `tests/` directory contains sample Ansible roles used for testing the generator.
