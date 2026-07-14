# API

The API is built with FastAPI. It follows REST conventions and uses Pydantic for request/response validation.

## OpenAPI

When the application is running, the interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Root

```http
GET /
```

Returns a Hello World message confirming the application is up.

### Health

```http
GET /health
```

Reports application and database connection status.

### Regions

#### Create a region

```http
POST /regions
```

Request body:

```json
{
  "name": "Cairo",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [31.0, 30.0],
        [31.5, 30.0],
        [31.5, 30.5],
        [31.0, 30.5],
        [31.0, 30.0]
      ]
    ]
  }
}
```

Returns the created region with its generated `id` and `created_at` timestamp. The geometry must be valid GeoJSON.

#### List all regions

```http
GET /regions
```

Returns an array of regions.

#### Get a region by ID

```http
GET /regions/{region_id}
```

Returns a single region. Responds with `404 Not Found` if the region does not exist.

#### Update a region

```http
PUT /regions/{region_id}
```

Request body accepts the same GeoJSON shape as `POST /regions`, but all fields are optional. Only provided fields are updated. Responds with `404 Not Found` if the region does not exist, or `422 Unprocessable Entity` if the geometry is invalid.

#### Delete a region

```http
DELETE /regions/{region_id}
```

Removes a region. Responds with `204 No Content` on success, or `404 Not Found` if the region does not exist.

## Status Codes

- `200 OK` for successful read or update operations.
- `201 Created` for successful creation.
- `204 No Content` for successful deletion.
- `404 Not Found` when a region is not found.
- `422 Unprocessable Entity` when the request body contains invalid geometry.
