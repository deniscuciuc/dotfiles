# External encrypted backups

Restic encrypts the repository. Store the password in your password manager and keep a separate recovery copy. The workstation's disk passphrase and its backup password are separate.

## Configure once

1. Attach the external drive. Use `lsblk -f` and `findmnt` to identify its **mount point and filesystem UUID**. Do not format the Archive HDD or use the system SSD as its own backup.
2. Create a private password file outside Git. Its parent directory and file should be readable only by your account (`0700` / `0600`). Avoid putting the password directly in shell history.
3. Create `~/.config/workstation/backup.conf` with mode `0600`, replacing the example paths:

   ```bash
   BACKUP_MOUNT='/media/your-user/ExternalBackup'
   BACKUP_UUID='replace-with-the-external-filesystem-uuid'
   RESTIC_REPOSITORY="$BACKUP_MOUNT/restic/ubuntu-workstation"
   RESTIC_PASSWORD_FILE="$HOME/.config/workstation/restic-password"
   ```

4. Review `~/.config/workstation/backup-targets.txt`. Its relative entries are always relative to your home, even when you run the command inside another project. Add any projects stored elsewhere using absolute paths.

## Use

```bash
ws-backup init             # Only for a new repository
ws-backup backup
ws-backup snapshots
ws-backup check
ws-backup restore latest /tmp/my-new-restore-test
```

The configured drive must be mounted; when a UUID is supplied it must match. This avoids silently backing up into an empty mount directory on the system disk. Restore requires a new absolute destination and never overwrites your working home.

Run a backup from an unrelated directory such as `/tmp` and verify that the intended home/project paths still appear in `ws-backup snapshots`. Perform a restore test and compare representative files. `ws-backup check` uses Restic's `--read-data` option to verify stored content as well as metadata; a large repository can take considerable time.

Missing optional target folders are reported. Resolve unexpectedly missing important folders before relying on the backup. If all targets are missing, backup fails. Keep the password separately recoverable; a copy inside the encrypted backup cannot unlock that backup.

## Databases and cleanup

Create consistent logical database dumps and include their directory in the targets. Raw live database/container storage is excluded; backing it up while running is not a substitute for a verified database export. Include object-storage uploads through their service export or a consistent stopped-volume backup.

Configuration and AI histories are retained in the encrypted backup. Rebuildable Node/Python dependencies, container layers and tool caches are excluded.

Retention is a separate, deliberate action:

```bash
ws-backup retention        # Show instructions; makes no changes
ws-backup retention --apply
```

The applied policy retains 7 daily, 4 weekly and 12 monthly snapshots, then prunes unreferenced data. No backup command runs retention automatically. ws-setup's workstation maintenance module schedules daily backups and weekly integrity checks; this dotfiles repository supplies their helpers but does not enable timers itself. Use `ws-maintenance backup` for manual runs that update backup freshness tracking. See [maintenance](https://github.com/deniscuciuc/ws-setup/blob/main/docs/MAINTENANCE.md).
