from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    geometry: Mapped[Geometry] = mapped_column(
        Geometry("POLYGON", srid=4326),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
