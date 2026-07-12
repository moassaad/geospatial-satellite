# Project Structure

```text
app/
    main.py

    config/
    core/
    database/
    dependencies/
    models/
    repositories/
    routers/
    schemas/
    services/
    utils/

tests/

docker/

sample_data/

docs/

README.md
.env.example
requirements.txt
docker-compose.yml
```

## Architecture

The application follows a layered architecture:

- **Routers** handle HTTP requests and routing.
- **Services** contain business logic.
- **Repositories** communicate with the database.
- **Models** describe database entities.
- **Schemas** validate incoming requests and outgoing responses.

Business logic only lives inside services. Routers remain thin and delegate work to the appropriate service.
