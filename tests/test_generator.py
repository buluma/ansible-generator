import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent
PRE_COMMIT_DISABLED = {"generate_pre_commit": False}


class GeneratorTests(unittest.TestCase):
    def clean_role(self, fixture):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        source = FIXTURES / fixture
        role = Path(directory.name) / fixture
        for name in (
            "meta/main.yml",
            "meta/preferences.yml",
            "defaults/main.yml",
            "requirements.yml",
            "molecule/default/converge.yml",
            "molecule/default/prepare.yml",
            "molecule/default/verify.yml",
        ):
            if (source / name).is_file():
                destination = role / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / name, destination)
        return role

    def generate(self, role, **settings):
        existing_yaml = set(role.rglob("*.yml")) | set(role.rglob("*.yaml"))
        settings = {
            **PRE_COMMIT_DISABLED,
            "role_path": str(role),
            "ansible_python_interpreter": sys.executable,
            **settings,
        }
        result = subprocess.run(
            [
                "ansible-playbook",
                str(ROOT / "generate.yml"),
                "-i", "localhost,",
                "-c", "local",
                "--extra-vars",
                json.dumps(settings),
            ],
            cwd=role,
            capture_output=True,
            text=True,
            timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        generated_yaml = (set(role.rglob("*.yml")) | set(role.rglob("*.yaml"))) - existing_yaml
        if generated_yaml:
            lint = subprocess.run(
                ["yamllint", "--strict", "-c", str(ROOT / ".yamllint"), *sorted(generated_yaml)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        return result.stdout

    def test_fixtures(self):
        for fixture in sorted(FIXTURES.glob("ansible-role-*")):
            with self.subTest(fixture=fixture.name):
                role = self.clean_role(fixture.name)
                self.generate(role)
                for path in (
                    "README.md",
                    "molecule/default/molecule.yml",
                    ".github/workflows/molecule.yml",
                    ".github/workflows/requirements2png.yml",
                ):
                    self.assertTrue((role / path).is_file(), path)
                for path in (".gitlab-ci.yml", ".pre-commit-config.yaml", ".github/FUNDING.yml"):
                    self.assertFalse((role / path).exists(), path)

                workflow = yaml.safe_load((role / ".github/workflows/molecule.yml").read_text())
                job = workflow["jobs"]["molecule"]
                matrix = job["strategy"]["matrix"]["distro"]
                self.assertIn({"image": "docker-molecule-images", "tag": "debian13"}, matrix)
                self.assertEqual(job["steps"][0]["with"]["path"], fixture.name)
                if fixture.name == "ansible-role-default":
                    self.assertRegex(self.generate(role), r"changed=0\s+unreachable=0\s+failed=0")
                if fixture.name == "ansible-role-preferences":
                    env = next(step["env"] for step in job["steps"] if step["name"] == "Test with molecule")
                    self.assertEqual(env["VAULT_LICENCE"], "${{ secrets.VAULT_LICENSE }}")
                    self.assertEqual(env["someTHING"], "${{ secrets.MY_VAR }}")
                    molecule = yaml.safe_load((role / "molecule/default/molecule.yml").read_text())
                    self.assertNotIn("env", molecule["provisioner"])

    def test_gitlab_and_github_share_platform_matrix_with_gitlab_overrides(self):
        role = self.clean_role("ansible-role-default")
        self.generate(
            role,
            generate_gitlab_ci="yes",
            platforms=[{"name": "Debian", "versions": ["trixie"]}],
            molecule_matrix_include=[{"tag": "debian13"}, {"tag": "extra"}],
        )
        github = yaml.safe_load((role / ".github/workflows/molecule.yml").read_text())
        gitlab = yaml.safe_load((role / ".gitlab-ci.yml").read_text())
        expected = [{"image": "docker-molecule-images", "tag": "debian13"}]
        self.assertEqual(github["jobs"]["molecule"]["strategy"]["matrix"]["distro"], expected)
        self.assertEqual(
            gitlab["molecule"]["parallel"]["matrix"],
            expected + [{"image": "docker-molecule-images", "tag": "extra"}],
        )

    def test_requirements_workflow_can_be_generated_on_its_own(self):
        role = self.clean_role("ansible-role-minimal")
        self.generate(
            role,
            generate_github_settings="no",
            generate_github_action_molecule=False,
            generate_github_action_galaxy=False,
            generate_github_action_todo=False,
            generate_github_issue_template=False,
            generate_github_feature_template=False,
        )
        workflows = role / ".github/workflows"
        self.assertEqual({file.name for file in workflows.iterdir()}, {"requirements2png.yml"})
