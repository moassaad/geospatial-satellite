# Spatial Queries

The API can run spatial queries directly in PostGIS, taking advantage of the geometry index on the `regions` table.

## Containment Query

### `POST /contains`

Returns every region whose geometry contains a given point.

Request body:

```json
{
  "latitude": 30.0444,
  "longitude": 31.2357
}
```

Response:

```json
[
  {
    "id": 1,
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
    },
    "created_at": "2026-07-14T20:04:01.587378Z"
  }
]
```

If the point falls outside every region, the endpoint returns an empty list.

## Implementation

The query uses `ST_Contains` to test whether each region's geometry contains the supplied point. The point is constructed with `ST_GeomFromText` using SRID 4326, matching the geometry column's spatial reference system.

## Example

```bash
curl -X POST http://localhost:8000/contains \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.0444, "longitude": 31.2357}'
```

## Intersection Query

### `POST /intersects`

Returns every region whose geometry intersects a given point.

Request body:

```json
{
  "latitude": 30.0,
  "longitude": 31.0
}
```

Response:

```json
[
  {
    "id": 1,
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
    },
    "created_at": "2026-07-14T20:04:01.587378Z"
  }
]
```

If the point does not intersect any region, the endpoint returns an empty list.

The query uses `ST_Intersects` to test whether each region's geometry intersects the supplied point. The point is constructed with `ST_GeomFromText` using SRID 4326, matching the geometry column's spatial reference system.

```bash
curl -X POST http://localhost:8000/intersects \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.0, "longitude": 31.0}'
```
