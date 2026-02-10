# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy requirements.txt (Now confirmed in your root!)
COPY requirements.txt .

# 2. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your application code
COPY . .

# 4. Expose the port for Hugging Face
EXPOSE 7860

# 5. Run the application (Pointing to main.py)
CMD ["streamlit", "run", "main.py", "--server.port=7860", "--server.address=0.0.0.0"]