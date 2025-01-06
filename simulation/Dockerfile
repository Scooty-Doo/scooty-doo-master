FROM python:3.10-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../src /app/src
COPY ./src /app/simulation/src
COPY ./requirements.txt /app/simulation/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/simulation/requirements.txt

# Set environment variables (can be overridden by docker-compose)
ENV PYTHONPATH=/app

CMD ["python", "-m", "simulation.src.main"]
