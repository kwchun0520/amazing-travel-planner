FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements (if you have a requirements.txt in project root)
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the tools directory into the container
COPY . .

# Expose the port (change if your server uses a different port)
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]