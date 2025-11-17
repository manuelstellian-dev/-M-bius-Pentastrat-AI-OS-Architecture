FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all services
COPY services/ /app/services/

# Service to run is passed as build arg
ARG SERVICE
ENV SERVICE_NAME=${SERVICE}

# Default command - will be overridden by docker-compose
CMD python -m services.${SERVICE_NAME}.main
