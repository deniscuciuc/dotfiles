import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "dot_local/bin/executable_ws-maintenance"


class Maintenance(unittest.TestCase):
    def fixture(self, root):
        home = Path(root)
        (home/".local/bin").mkdir(parents=True)
        (home/".config/workstation").mkdir(parents=True)
        config = home/".config/workstation/backup.conf"
        config.write_text("BACKUP_MOUNT=/external-test\n")
        for name, source in {
            "mountpoint": '#!/bin/sh\nexit "${MOUNT_RC:-0}"\n',
            "ws-backup": '#!/bin/sh\necho called >> "$HOME/calls"\nexit "${BACKUP_RC:-0}"\n',
            "notify-send": '#!/bin/sh\necho notified >> "$HOME/notifications"\n',
            "df": '#!/bin/sh\nprintf "header\\nfs 1000000000 1 999999999 1%% /\\n"\n',
        }.items():
            path=home/".local/bin"/name
            path.write_text(source)
            path.chmod(0o755)
        return dict(os.environ, HOME=str(home), XDG_STATE_HOME=str(home/"state"), XDG_CONFIG_HOME=str(home/".config"), PATH=str(home/".local/bin")+":"+os.environ["PATH"])

    def call(self, env, action):
        return subprocess.run(["bash", str(TOOL), action], env=env, capture_output=True, text=True)

    def test_absent_disk_skips_without_success_marker(self):
        with tempfile.TemporaryDirectory() as root:
            env=self.fixture(root)
            env["MOUNT_RC"]="1"
            self.assertEqual(self.call(env,"backup").returncode,0)
            self.assertFalse(Path(root,"calls").exists())
            self.assertFalse(Path(root,"state/ws-maintenance/backup.success").exists())

    def test_failures_and_success_are_distinguished(self):
        with tempfile.TemporaryDirectory() as root:
            env=self.fixture(root)
            env["BACKUP_RC"]="3"
            self.assertEqual(self.call(env,"backup").returncode,3)
            marker=Path(root,"state/ws-maintenance/backup.success")
            self.assertFalse(marker.exists())
            env["BACKUP_RC"]="0"
            self.assertEqual(self.call(env,"backup").returncode,0)
            self.assertTrue(marker.exists())

    def test_health_notifies_only_on_state_change(self):
        with tempfile.TemporaryDirectory() as root:
            env=self.fixture(root)
            for _ in range(2): self.assertEqual(self.call(env,"health").returncode,0)
            self.assertEqual(Path(root,"notifications").read_text().splitlines(),["notified"])
            self.assertEqual(self.call(env,"backup").returncode,0)
            self.assertEqual(self.call(env,"health").returncode,0)
            self.assertFalse(Path(root,"state/ws-maintenance/backup.alert").exists())

    def test_backup_lock_prevents_overlapping_operations(self):
        import fcntl
        with tempfile.TemporaryDirectory() as root:
            env=self.fixture(root)
            state=Path(root,"state/ws-maintenance")
            state.mkdir(parents=True)
            with (state/"backup.lock").open("w") as lock:
                fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.assertEqual(self.call(env,"check").returncode,0)
                self.assertFalse(Path(root,"calls").exists())


if __name__ == "__main__": unittest.main()
