# PostGIS

The project uses the PostGIS spatial extension for PostgreSQL. It is enabled automatically when the database container is initialized for the first time.

## Initialization

The `db` service in `docker-compose.yml` mounts the `docker/initdb/` directory into the PostgreSQL initialization path `/docker-entrypoint-initdb.d/`. PostgreSQL executes any SQL scripts found there when the data directory is empty.

### Init Script

`docker/initdb/01_init_postgis.sql`:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Verification

After starting the database service, verify that PostGIS is installed and active:

```bash
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT PostGIS_Version();"
```

If the extension is enabled, the command returns the installed PostGIS version.

## Notes

- Init scripts only run when the `postgres_data` volume is empty.
- If you need to re-run the script, remove the volume first with `docker compose down -v`.
- The image `postgis/postgis:16-3.4` already bundles PostGIS; the init script only creates the extension inside the database.
