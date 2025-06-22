FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements (assumes requirements.txt is in project root)
COPY ../../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory to the container
COPY ../../src ./src

# Set environment variable for Streamlit
ENV PYTHONPATH=/app

# Accept GOOGLE_API_KEY as an environment variable at runtime
ENV GOOGLE_API_KEY=""

EXPOSE 8501

CMD ["streamlit", "run", "./src/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]