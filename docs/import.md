# GeoJSON Import

The GeoJSON import endpoint accepts a GeoJSON file upload.

The file is validated, but not persisted. Future sprints will parse and store the imported regions.

## Endpoint

```http
POST /import/geojson
```

- Content-Type: `multipart/form-data`
- Form field: `file` (required)
- Supported extensions: `.geojson`, `.json`
- Supported content types: `application/json`, `application/geo+json`
- Maximum file size: 10 MB

## Response

`202 Accepted`

```json
{
  "filename": "regions.geojson",
  "content_type": "application/geo+json",
  "size": 1234,
  "message": "GeoJSON file accepted for import"
}
```

## Errors

| Status | Description |
|--------|-------------|
| `422 Unprocessable Entity` | Missing file, unsupported extension, invalid content type, exceeds size limit, invalid JSON, or invalid GeoJSON object |

## Example

```bash
curl -X POST \
  -F file=@sample_data/regions.geojson \
  http://localhost:8000/import/geojson
```
