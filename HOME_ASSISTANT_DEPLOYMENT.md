# Home Assistant deployment

## One-time GitHub setup

Commit these deployment files to the public `mmaged92/MoneyNut` repository and
push `main`. In GitHub, open **Actions** and confirm **Publish Home Assistant
image** succeeds. Then open the package settings for
`ghcr.io/mmaged92/moneynut-amd64` and make the package public.

Add this repository to Home Assistant's app store:

`https://github.com/mmaged92/MoneyNut`

## One-time database migration

1. Create and download a full Home Assistant backup.
2. Stop the currently installed local MoneyNut app.
3. Through Samba, copy
   `addon_configs/local_moneynut/db.sqlite3` to
   `share/moneynut-db.sqlite3`. If the app-config folder has a slightly
   different name, use the one containing MoneyNut's live `db.sqlite3`.
4. Install the GitHub-provided MoneyNut app and start it. The startup log must
   report that it imported `/share/moneynut-db.sqlite3`.
5. Verify accounts, balances, and transactions. Create a new Home Assistant
   backup, then delete the temporary `share/moneynut-db.sqlite3` copy.
6. Only after verification, uninstall the old local MoneyNut app and remove its
   folder from `local_apps`/`addons`.

## Publishing an update

1. Make and test the Django changes.
2. Increment `version` in `homeassistant/config.yaml`, for example from `1.0.0`
   to `1.0.1`.
3. Commit and push to `main`.
4. Wait for the GitHub Actions workflow to finish.
5. In Home Assistant, check for app updates and select **Update**.

Never commit a SQLite database, `.env` file, email password, or Django secret.
