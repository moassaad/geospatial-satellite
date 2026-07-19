# GeoJSON Import

The GeoJSON import endpoint accepts a GeoJSON file upload and parses it using GeoPandas. The imported regions are not persisted yet.

## Endpoint

```http
POST /import/geojson
```

- Content-Type: `multipart/form-data`
- Form field: `file` (required)
- Supported extensions: `.geojson`, `.json`
- Supported content types: `application/json`, `application/geo+json`
- Maximum file size: 10 MB
- Supported geometries: `Polygon`, `MultiPolygon`
- Geometries are standardized to `EPSG:4326`

## Response

`202 Accepted`

```json
{
  "filename": "regions.geojson",
  "content_type": "application/geo+json",
  "size": 1234,
  "message": "GeoJSON file parsed successfully",
  "feature_count": 27,
  "columns": ["name", "code"],
  "crs": "EPSG:4326"
}
```

## Errors

| Status | Description |
|--------|-------------|
| `422 Unprocessable Entity` | Missing file, unsupported extension, invalid content type, exceeds size limit, invalid JSON, invalid GeoJSON, unsupported geometry type, missing CRS, or invalid geometries |

## Example

```bash
curl -X POST \
  -F file=@sample_data/regions.geojson \
  http://localhost:8000/import/geojson
```
