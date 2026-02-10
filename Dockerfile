FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PORT=7860
RUN apt-get update && apt-get install -y build-essential curl git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY . .
RUN python mcp_server/src/database.py
EXPOSE 7860
CMD ["uv", "run", "streamlit", "run", "agent_engine/src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
