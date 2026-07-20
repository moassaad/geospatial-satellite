"""alter region geometry type to GEOMETRY

Revision ID: 11ff040af578
Revises: da420b8cab2e
Create Date: 2026-07-19 21:13:15.000000
"""

from typing import Sequence, Union

from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa


revision: str = "11ff040af578"
down_revision: Union[str, None] = "da420b8cab2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "regions",
        "geometry",
        type_=Geometry(srid=4326),
        existing_type=Geometry(geometry_type="POLYGON", srid=4326),
        postgresql_using="geometry::geometry",
    )
    op.create_index(
        "idx_regions_geometry",
        "regions",
        ["geometry"],
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("idx_regions_geometry", table_name="regions")
    op.alter_column(
        "regions",
        "geometry",
        type_=Geometry(geometry_type="POLYGON", srid=4326),
        existing_type=Geometry(srid=4326),
    )
