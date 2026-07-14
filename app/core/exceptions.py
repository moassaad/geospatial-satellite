class RegionNotFoundError(Exception):
    def __init__(self, region_id: int) -> None:
        super().__init__(f"Region {region_id} not found")
        self.region_id = region_id


class InvalidGeometryError(Exception):
    pass
