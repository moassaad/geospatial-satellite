FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd --create-home appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Copy entrypoint and make it executable (as root)
COPY --chmod=755 docker/scripts/entrypoint.sh /entrypoint.sh

# Change ownership of application files
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]