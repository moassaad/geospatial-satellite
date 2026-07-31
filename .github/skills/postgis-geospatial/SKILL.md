---
name: postgis-geospatial
description: Enforces PostGIS best practices, spatial data types, SRID standardization, GeoJSON policies, and efficient spatial querying using GeoAlchemy2. Apply this when writing spatial models, database queries, or geospatial logic.
---

# PostGIS & Geospatial Guidelines

## Guiding Principles

- **Let PostGIS do the heavy lifting:** Spatial operations (filtering, measuring, intersecting) must be executed in the database. Never fetch raw geometries into Python to perform spatial calculations in memory.
- **Geospatial correctness is more important than convenience.** Performance should come from PostGIS, not application-side optimization.

## Coordinate Reference System (CRS) & SRID

- **Standard CRS:** All geometries stored in the database must use `SRID=4326`.
- **Constants:** Centralize SRID values as constants. Avoid hardcoding `4326` throughout the project.
- **SRID Transformation:** If incoming geometries use a different SRID, transform them before persistence using `ST_Transform`. Never store mixed SRIDs in the same column.
- **CRS Rule:** Avoid transforming geometries repeatedly. Transform once. Store once. Query consistently.
- **Coordinate Order:** Always enforce `(Longitude, Latitude)` order.

## Geometry vs Geography & Precision

- **Type Usage:** Use `Geometry` for standard spatial relationships. Use `Geography` strictly when calculating accurate distances or areas over the earth's curved surface (meters).
- **Coordinate Precision:** Preserve input precision. Do not round coordinates unless explicitly requested.

## Spatial Data Types & Nullability

- **Domain Matching:** Choose the geometry type that matches the domain. Use `Polygon` for guaranteed single polygons. Use `MultiPolygon` when multiple disconnected geometries are expected.
- **Null Geometry:** Geometry columns should be `NOT NULL` unless the domain explicitly allows missing geometries.
- **Regions of Interest (ROI):** Regions should be represented as `Polygon` or `MultiPolygon` geometries. Point coordinates used for containment checks must always be created with the configured SRID before executing spatial predicates.

## Geometry Creation & Updates

- **Creation:** Prefer database functions such as `ST_GeomFromGeoJSON` and `ST_GeomFromText` instead of constructing geometries manually in Python.
- **Updates:** Avoid updating geometry columns unless the geometry actually changes.

## Architecture & Repository Rules

- **Boundaries:** Spatial queries belong in repositories. Routers and services should never build PostGIS expressions.
- **Performance:** Return only required geometry representations. Avoid selecting geometry columns when they are not needed.
- **Serialization:** Perform geometry serialization in the database whenever possible (e.g., using `ST_AsGeoJSON`). Avoid converting WKB to GeoJSON in Python unless transformation is required.

## Spatial Predicates & Filtering

- **Bounding Box:** Bounding-box filtering should be used whenever possible. Allow PostGIS to leverage spatial indexes before exact geometry evaluation.
- **Predicates:**
  - Prefer `ST_Intersects` for overlap detection.
  - Prefer `ST_Contains` when the boundary must fully contain another geometry.
  - Prefer `ST_Within` when checking if one geometry is inside another.
  - Prefer `ST_Equals` only when exact geometry equality is required.

## Spatial Indexing

- **Mandatory Indexes:** Every spatial column MUST have a GIST (Generalized Search Tree) index.

## Data Validation & GeoJSON Policy

- **Validation:** Reject invalid geometries before persistence whenever possible. Do not defer validation to later processing stages.
- **GeoJSON Formatting:** `FeatureCollection` should be used only when returning collections. Single resources should return a single `Feature`.

## AI Decision Rules

If multiple spatial implementations are valid, prefer the implementation that:

1. Executes inside PostGIS.
2. Minimizes transferred geometry.
3. Leverages spatial indexes.
4. Minimizes coordinate transformations.

## Self Review Checklist

- [ ] SRID mapped via constants (defaulting to 4326).
- [ ] Geometry type strictly matches domain requirements.
- [ ] GIST index is applied to the spatial column.
- [ ] Spatial queries isolated in Repositories.
- [ ] Geometries serialized via database functions (`ST_AsGeoJSON`).
- [ ] Validation occurs prior to persistence.
- [ ] Unneeded geometry columns are omitted from `SELECT` statements.
