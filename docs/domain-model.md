# Domain Model

## Region

The central entity is the `Region`, representing a geographic Region of Interest (ROI).

### Model

`app/models/region.py`

| Field      | Type                    | Description                                  |
|------------|-------------------------|----------------------------------------------|
| `id`       | Integer                 | Primary key, auto-incremented.               |
| `name`     | String                  | Human-readable name of the region.           |
| `geometry` | Geometry(POLYGON, 4326) | Polygon geometry stored in PostGIS (SRID 4326). |
| `created_at` | DateTime              | Timestamp when the record was created.       |

### Notes

- `geometry` uses GeoAlchemy2 `Geometry("POLYGON", srid=4326)` so that spatial queries can be run directly in PostGIS.
- `created_at` is populated automatically by the database using `func.now()`.
- The model inherits from the SQLAlchemy 2.0 `DeclarativeBase` defined in `app/database/base.py`.
