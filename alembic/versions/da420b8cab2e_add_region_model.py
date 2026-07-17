"""add region model

Revision ID: da420b8cab2e
Revises:
Create Date: 2026-07-13 22:21:39.151045
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = "da420b8cab2e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "regions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "geometry",
            Geometry(
                geometry_type="POLYGON",
                srid=4326,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_regions_id",
        "regions",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_regions_id", table_name="regions")
    op.drop_table("regions")