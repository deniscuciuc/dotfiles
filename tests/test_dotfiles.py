import json
import os
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Dotfiles(unittest.TestCase):
    def test_bitwarden_agent_wrapper_is_scoped_to_child(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = Path(directory, "snap/bitwarden/current/.bitwarden-ssh-agent.sock")
            agent.parent.mkdir(parents=True)
            tool = ROOT / "dot_local/bin/executable_ws-ssh-agent"
            env = dict(os.environ, HOME=directory, SSH_AUTH_SOCK="/forwarded/agent")
            missing = subprocess.run(["bash", str(tool)], env=env, text=True, capture_output=True)
            self.assertNotEqual(missing.returncode, 0)
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(str(agent))
                result = subprocess.run(["bash", str(tool), "sh", "-c", 'printf "%s" "$SSH_AUTH_SOCK"'], env=env, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, str(agent))
                self.assertEqual(env["SSH_AUTH_SOCK"], "/forwarded/agent")

    def test_modify_scripts_preserve_customization(self):
        for name in ["modify_dot_bashrc", "modify_dot_profile"]:
            original = 'export MY_CUSTOM_SETTING="keep me"\n'
            first = subprocess.check_output(["python3", str(ROOT / name)], input=original, text=True)
            second = subprocess.check_output(["python3", str(ROOT / name)], input=first, text=True)
            self.assertIn(original, first)
            self.assertEqual(first, second)

    def test_shell_is_quiet_noninteractively(self):
        result = subprocess.run(["bash", "-c", 'source "$1"; printf ok', "bash", str(ROOT / "private_dot_config/bash/workstation.bash")], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "ok")
        self.assertEqual(result.stderr, "")

    def test_standard_commands_are_not_replaced(self):
        result = subprocess.run(["bash", "-c", 'source "$1"; ! alias cat find grep ls 2>/dev/null', "bash", str(ROOT / "private_dot_config/bash/aliases.bash")])
        self.assertEqual(result.returncode, 0)

    def test_json_configs(self):
        for path in ROOT.rglob("*.json"):
            json.loads(path.read_text())

    def test_backup_paths_do_not_depend_on_working_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp, "home")
            home.mkdir()
            (home / "Documents").mkdir()
            bin_dir = Path(temp, "bin")
            bin_dir.mkdir()
            mount = Path(temp, "external")
            mount.mkdir()
            password = Path(temp, "password")
            password.write_text("test-only")
            targets = Path(temp, "targets")
            targets.write_text("Documents\n~/Documents\n# comment\nmissing\n")
            excludes = Path(temp, "excludes")
            excludes.write_text("")
            config = Path(temp, "backup.conf")
            config.write_text(f'BACKUP_MOUNT="{mount}"\nRESTIC_REPOSITORY="{mount}/repo"\nRESTIC_PASSWORD_FILE="{password}"\nBACKUP_TARGETS_FILE="{targets}"\nBACKUP_EXCLUDES_FILE="{excludes}"\n')
            output = Path(temp, "args.json")
            for name, content in {
                "mountpoint": "#!/bin/sh\nexit 0\n",
                "restic": '#!/usr/bin/env python3\nimport json,os,sys\nopen(os.environ["ARGS"],"w").write(json.dumps(sys.argv[1:]))\n',
            }.items():
                executable = bin_dir / name
                executable.write_text(content)
                executable.chmod(0o755)
            env = dict(os.environ, HOME=str(home), WS_BACKUP_CONFIG=str(config), ARGS=str(output), PATH=str(bin_dir) + ":" + os.environ["PATH"])
            tool = ROOT / "dot_local/bin/executable_ws-backup"
            result = subprocess.run(["bash", str(tool), "backup"], cwd="/tmp", env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            args = json.loads(output.read_text())
            self.assertEqual(args[-2:], [str(home / "Documents")] * 2)
            # A mount-prefix string must not allow symlinks to route data onto the OS disk.
            (mount / "repo").symlink_to(home, target_is_directory=True)
            output.unlink()
            result = subprocess.run(["bash", str(tool), "backup"], cwd="/tmp", env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            (mount / "repo").unlink()
            (bin_dir / "mountpoint").write_text("#!/bin/sh\nexit 1\n")
            result = subprocess.run(["bash", str(tool), "backup"], cwd="/tmp", env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
