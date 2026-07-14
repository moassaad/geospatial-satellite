# Repositories

Repositories are the only layer that talks to the database. They encapsulate persistence logic and return SQLAlchemy model instances so that services do not need to interact directly with the database session.

## Region Repository

`app/repositories/region_repository.py` exposes CRUD operations for the `Region` model.

### Operations

- `get_all(db)` — returns every region.
- `get_by_id(db, region_id)` — returns a single region or `None` if it does not exist.
- `create(db, data)` — creates a new region from a `RegionCreate` schema, commits, and refreshes it.
- `update(db, region, data)` — applies changes from a `RegionUpdate` schema, commits, and refreshes it.
- `delete(db, region)` — removes a region and commits the transaction.

Each function receives a SQLAlchemy `Session` that is managed by the caller (usually a service). This keeps transactions explicit and prevents persistence logic from leaking into other layers.

## Geometry Handling

The repository converts GeoJSON geometry dictionaries into GeoAlchemy2 geometry objects using Shapely and `geoalchemy2.shape.from_shape`. This translation belongs in the repository because it is part of persisting the data correctly in PostGIS.
