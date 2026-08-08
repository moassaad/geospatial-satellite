---
name: geopandas
description: Enforces GeoPandas best practices for spatial data processing, I/O operations, CRS conversion, geometry validation, and data cleaning. Apply when writing Python scripts or services that ingest or prepare spatial files.
---

# GeoPandas & Spatial Data Processing Guidelines

## Guiding Principles
* **GeoPandas prepares spatial data. PostGIS analyzes spatial data. Repositories persist spatial data.**
* GeoPandas is for data processing, not database transactions. Do not use GeoPandas to directly insert data into the database.

## Supported Formats & File Validation
* **Formats:** Support only the spatial formats required by the project (e.g., GeoJSON, Shapefile). Do not add parsers for additional formats unless explicitly requested.
* **File Validation:** Validate uploaded files before reading. Verify:
  - File extension
  - File existence
  - File size
  - Required Shapefile components (`.shp`, `.dbf`, `.shx`, `.prj` when applicable)

## CRS (Coordinate Reference System) Management
* **Never Guess:** Always check `gdf.crs` immediately after reading a file. Never guess the CRS. If the source CRS cannot be determined, fail with a clear validation error.
* **Standardization:** Transform all incoming geometries to `EPSG:4326` using `gdf.to_crs(epsg=4326)` BEFORE passing the data to the repository.
* **Consistency:** Never mix different CRSs in the same GeoDataFrame.

## Geometry & Type Validation
* **Active Column:** Always ensure the active geometry column is correctly configured before spatial operations.
* **Geometry Types:** Validate geometry types before processing. Reject unsupported geometry types early.
* **Missing & Empty:** Handle missing geometries. Filter out empty geometries unless the domain explicitly requires them.
* **Validity Checks:** Use `gdf.is_valid` to identify invalid geometries. Apply `.make_valid()` to correct topological errors automatically before processing.

## Attribute Cleaning & Duplicates
* **Attributes:** Normalize attribute names when necessary. Trim whitespace. Handle missing attribute values consistently. Avoid silently dropping important attributes.
* **Duplicates:** Remove duplicate features only when duplicates are truly identical and the domain allows deduplication.
* **Mutability:** Avoid mutating the original GeoDataFrame unnecessarily. Prefer creating transformed copies when readability improves.

## Performance, Indexes & Memory
* **Vectorization:** Prefer vectorized operations for spatial processing. Use row iteration only when converting processed features into application objects and no vectorized alternative exists.
* **Spatial Index:** Use the GeoPandas spatial index when repeatedly querying large GeoDataFrames.
* **Large Files:** Avoid loading unnecessarily large datasets into memory. Process incrementally when appropriate.

## Architecture & Boundaries
* **Service Layer:** GeoPandas processing belongs only to data ingestion services. Business services should not manipulate GeoDataFrames.
* **Repository Layer:** Repositories should receive plain Python values (e.g., WKT strings or dictionaries). Never pass entire GeoDataFrames across application layers.

## Error Handling & Logging
* **Logging:** Log file metadata such as feature count and detected CRS. Do not log geometry contents.
* **Exceptions:** Catch specific exceptions raised by the underlying geospatial libraries. Translate them into meaningful domain errors.

## AI Decision Rules
If multiple GeoPandas implementations are valid, prefer the implementation that:
1. Minimizes memory usage.
2. Preserves CRS correctness.
3. Avoids geometry mutation.
4. Uses vectorized operations.

## Self Review Checklist
- [ ] File extensions and components (e.g., Shapefile dependencies) are validated.
- [ ] CRS is strictly identified, never guessed, and transformed to EPSG:4326.
- [ ] Unsupported geometry types are rejected early.
- [ ] Repositories receive standard Python objects, not GeoDataFrames.
- [ ] Metadata (not geometry) is logged.