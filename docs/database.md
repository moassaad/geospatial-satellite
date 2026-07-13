# Database

The application uses SQLAlchemy 2.0 as the ORM with PostgreSQL. Session management follows the dependency-injection pattern used by FastAPI.

## Engine and Session

Database connectivity is configured in `app/database/database.py`.

- `engine`: created from `DATABASE_URL` via Pydantic Settings.
- `SessionLocal`: a session factory bound to the engine.
- `get_db()`: a generator dependency that yields a SQLAlchemy `Session` and ensures it is closed after the request.

## Declarative Base

`app/database/base.py` defines the SQLAlchemy `DeclarativeBase` subclass used by all ORM models.

## Usage in Endpoints

Inject a database session using FastAPI `Depends`:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db

@router.get("/example")
def example(db: Session = Depends(get_db)):
    ...
```

## Environment Variables

The `DATABASE_URL` value is loaded from `.env` by `app.config.settings.Settings`.
