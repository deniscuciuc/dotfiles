import os
from pathlib import Path
import subprocess
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / "dot_local/bin/executable_ws-storage"


class Storage(unittest.TestCase):
    def command(self, root, store, probe=False):
        binary=root/"bin"
        binary.mkdir(exist_ok=True)
        fake=binary/"pnpm"
        fake.write_text('#!/bin/sh\nif [ "$1" = store ]; then printf "%s\\n" "$TEST_STORE"; else printf "auto\\n"; fi\n')
        fake.chmod(0o755)
        project=root/"project"
        project.mkdir(exist_ok=True)
        env=dict(os.environ, TEST_STORE=str(store), PATH=str(binary)+":"+os.environ["PATH"])
        return subprocess.run(["python3",str(TOOL),"pnpm",str(project),*(["--probe"] if probe else [])], env=env,text=True,capture_output=True)

    def test_probe_checks_links_and_cleans_temporary_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            store=root/"store"
            store.mkdir()
            result=self.command(root,store,True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn("Hardlink probe passed",result.stdout)
            self.assertEqual(list(store.iterdir()),[])
            self.assertEqual(list((root/"project").iterdir()),[])

    def test_cross_filesystem_store_fails(self):
        if not Path('/dev/shm').is_dir(): self.skipTest('Linux shared memory filesystem required')
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory(dir='/dev/shm') as other:
            if Path(directory).stat().st_dev == Path(other).stat().st_dev: self.skipTest('Need separate filesystems')
            result=self.command(Path(directory),Path(other))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('different filesystems',result.stderr)

    def test_read_only_check_does_not_create_missing_store(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            store=root/'missing/store'
            result=self.command(root,store)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertFalse(store.exists())


if __name__ == '__main__': unittest.main()
