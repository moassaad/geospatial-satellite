# Services

Services contain the business logic of the application. They orchestrate repositories, enforce domain rules, and raise domain exceptions. They never interact with the database directly.

## Region Service

`app/services/region_service.py` implements the business operations for regions.

### Operations

- `list_regions(db)` — returns every region by delegating to the repository.
- `get_region(db, region_id)` — returns a region or raises `RegionNotFoundError` if it does not exist.
- `create_region(db, data)` — validates the geometry and creates a new region.
- `update_region(db, region_id, data)` — loads the region, validates any new geometry, applies the update, and saves it.
- `delete_region(db, region_id)` — loads the region and removes it.

### Domain Exceptions

Defined in `app/core/exceptions.py`:

- `RegionNotFoundError`: raised when a requested region cannot be found.
- `InvalidGeometryError`: raised when the supplied GeoJSON geometry is invalid according to Shapely.

### Geometry Validation

Before a region is created or updated, the service validates the GeoJSON geometry using Shapely. Invalid or malformed geometry is rejected before it reaches the repository, keeping persistence concerns separated from validation.
