# MoneyNut

MoneyNut runs on port 8090. Its SQLite database and Django secret key are kept
in Home Assistant's persistent app data and are included in app backups.

On the first start only, the app imports `/share/moneynut-db.sqlite3` when that
file exists and its persistent database does not. Delete the import copy from
`share` after verifying the migration.

For remote access, route `home.moneynut.xyz` through Cloudflare Tunnel to
`http://192.168.4.27:8090` and protect it with Cloudflare Access.
