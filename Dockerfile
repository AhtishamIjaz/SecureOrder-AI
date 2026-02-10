FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file we generated
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Port 7860 is required for Hugging Face
EXPOSE 7860

# Start the application using main.py
CMD ["streamlit", "run", "main.py", "--server.port=7860", "--server.address=0.0.0.0"]