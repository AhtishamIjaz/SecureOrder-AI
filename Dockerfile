# 1. Base Image
FROM python:3.11-slim

# 2. Environment Setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860 \
    UV_PROJECT_ENVIRONMENT=/usr/local

# 3. System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Work Directory
WORKDIR /app

# 5. Install UV (The modern way)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 6. Install Dependencies First
# We copy ONLY these files first to take advantage of Docker Caching
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r <(uv pip compile pyproject.toml) || \
    uv pip install --system --no-cache streamlit langchain-openai fastmcp langgraph pydantic-settings sqlite3

# 7. Copy Project Files
COPY . .

# 8. Initialize Database (Logic Protection)
# This ensures the 'data' folder exists so SQLite doesn't crash
RUN mkdir -p mcp_server/data && python mcp_server/src/database.py

# 9. Hugging Face Requirements
EXPOSE 7860

# 10. Start Command
CMD ["streamlit", "run", "agent_engine/src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]