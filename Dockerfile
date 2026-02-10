FROM python:3.11-slim

WORKDIR /app

# Install system tools
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Copy uv for fast installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 1. Copy only the dependency files
COPY pyproject.toml uv.lock ./

# 2. Install dependencies (Clean and simple)
RUN uv pip install --system --no-cache .

# 3. Copy the rest of your app
COPY . .

# 4. Hugging Face port
EXPOSE 7860

# 5. Start the app
CMD ["streamlit", "run", "main.py", "--server.port=7860", "--server.address=0.0.0.0"]