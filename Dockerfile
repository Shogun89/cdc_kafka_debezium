FROM python:3.10

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire fastapi directory
COPY ./fastapi /app/fastapi

# Copy mysql-source.json and entrypoint.sh
COPY mysql-source.json /app/mysql-source.json
COPY entrypoint.sh /app/entrypoint.sh

# Make sure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
