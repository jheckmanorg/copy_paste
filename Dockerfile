FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make scripts executable
RUN chmod +x /app/scripts/migrate.sh

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default command (can be overridden)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
