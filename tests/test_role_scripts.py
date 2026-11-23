from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import clone_repos
import run_generator


class RoleScriptTests(unittest.TestCase):
    def test_clone_keeps_credentials_out_of_arguments_and_scopes_the_helper(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(clone_repos, "CLONE_DIR", directory),
            patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}),
            patch.object(clone_repos, "GH_TOKEN", "test-token"),
            patch.object(clone_repos.subprocess, "run") as clone,
            redirect_stdout(io.StringIO()),
        ):
            url = "https://github.com/example/ansible-role-demo.git"
            clone_repos.process_repo(
                {"name": "ansible-role-demo", "archived": False, "clone_url": url}
            )
            command = clone.call_args.args[0]
            self.assertIn(url, command)
            self.assertNotIn("test-token", " ".join(command))

        # Exercise Git's credential protocol locally without cloning or contacting GitHub.
        options = command[1:command.index("clone")]
        for host in ("github.com", "example.org"):
            with self.subTest(host=host):
                result = subprocess.run(
                    ["git", *options, "credential", "fill"],
                    input=f"protocol=https\nhost={host}\n\n",
                    capture_output=True,
                    text=True,
                    env={**os.environ, "GITHUB_TOKEN": "test-token", "GIT_TERMINAL_PROMPT": "0"},
                    timeout=10,
                )
                if host == "github.com":
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("password=test-token", result.stdout)
                else:
                    self.assertNotIn("test-token", result.stdout + result.stderr)

    def test_batch_skips_archives_and_reports_failures_after_processing_active_roles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("ansible-role-alpha", "ansible-role-beta", "archived-ansible-role-old", "other"):
                role = root / name
                (role / ".git").mkdir(parents=True)
                (role / "meta").mkdir()
                (role / "meta/main.yml").touch()
            (root / "ansible-role-noncheckout").mkdir()

            output = io.StringIO()
            with (
                patch.object(run_generator, "CLONE_DIR", root),
                patch.object(
                    run_generator.subprocess, "run",
                    side_effect=[subprocess.CalledProcessError(2, ["ansible-playbook"]), None],
                ) as run,
                redirect_stdout(output),
            ):
                self.assertEqual(run_generator.run_generator(), 1)
            self.assertEqual(
                [call.kwargs["cwd"].name for call in run.call_args_list],
                ["ansible-role-alpha", "ansible-role-beta"],
            )
            for call in run.call_args_list:
                self.assertEqual(json.loads(call.args[0][-1])["role_path"], str(call.kwargs["cwd"]))
            self.assertIn("Failed roles: ansible-role-alpha", output.getvalue())
