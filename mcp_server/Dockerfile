FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .
COPY mcp_server/requirements.txt ./mcp_server/
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r mcp_server/requirements.txt

# Copy application code
COPY mcp_server/ ./mcp_server/
COPY . .

# Create data directory
RUN mkdir -p mcp_server/data

# Expose MCP port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/mcp_server/data/orders.db

# Start MCP server
CMD ["python", "-m", "uvicorn", "mcp_server.src.server:app", "--host", "0.0.0.0", "--port", "8000"]
