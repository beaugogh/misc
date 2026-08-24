# WeChat backup formats

Use file structure, not folder names, to identify the input.

## Unencrypted iPhone Finder/iTunes backup

Typical root files include `Manifest.db`, `Manifest.plist`, `Info.plist`, and hashed payload directories such as `00` through `ff`.

Check encryption before export:

```bash
plutil -p "/path/to/backup/Manifest.plist" | grep IsEncrypted
```

`IsEncrypted = 0` is supported by the bundled exporter. A Finder backup is the preferred source when future arbitrary conversation exports are required because it retains WeChat's ordinary iOS databases and media catalog in a format the exporter already understands.

## Legacy WeChat desktop migration backup

Typical files:

- `Backup.db`
- `BAK_0_TEXT`, optionally additional `BAK_*_TEXT`
- `BAK_0_MEDIA`, optionally additional `BAK_*_MEDIA`

These containers are encrypted. `Backup.db` not opening in ordinary SQLite is expected. Direct conversion requires a compatible decryptor and the backup key; otherwise restore through a compatible, authorized WeChat client and create a new unencrypted Finder backup.

## Modern WeChat 4.x migration backup

Typical structure:

- `backup.attr`, `alt_name.dat`, and parent-level `roam_device_info.dat`
- `files/<generation>/<conversation-hash>/ChatPackage/...`
- `Index/...`
- `Media/*.tar.enc`

These are encrypted restore packages, not directly readable chat databases. Preserve the entire account-level tree including parent metadata if official WeChat restoration may be needed. Do not treat a readable HTML export as a bit-for-bit replacement for the raw encrypted archive when future recovery of unsupported objects matters.

## Safety and archival distinction

- Never test decryption or restoration against the only copy.
- Official restoration can change phone state; make a fresh device/Finder backup first and prefer a spare phone when practical.
- HTML/JSON/CSV are durable for reading and search, but may flatten unsupported cards, transfers, system objects, or proprietary media into placeholders.
- Retaining an unencrypted Finder backup gives more future extraction flexibility than retaining only selected HTML conversations.
