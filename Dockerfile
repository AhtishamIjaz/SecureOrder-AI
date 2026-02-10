# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install minimal system dependencies required for building some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy requirements.txt from your ROOT folder to the container
COPY requirements.txt .

# 2. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your application code into the container
COPY . .

# 4. Expose the port Streamlit uses by default on Hugging Face
EXPOSE 7860

# 5. Run the application
# Note: Replace 'app.py' with your actual main file name if it is different
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]