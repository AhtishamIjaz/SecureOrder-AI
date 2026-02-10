# 1. Use a stable base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies (needed for many Python libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy your requirements files specifically
# (Assuming you have these files in these folders)
COPY agent_engine/requirements.txt ./agent_engine/
COPY mcp_server/requirements.txt ./mcp_server/

# 5. Install Python packages
RUN pip install --no-cache-dir -r agent_engine/requirements.txt
RUN pip install --no-cache-dir -r mcp_server/requirements.txt
RUN pip install --no-cache-dir streamlit

# 6. Copy the entire project code
COPY . .

# 7. Logic Base: Create the data folder and initialize the database
# This ensures the DB exists before the app starts
RUN mkdir -p mcp_server/data
RUN python mcp_server/src/database.py

# 8. Hugging Face/Cloud port requirement
EXPOSE 7860

# 9. The command to run your app
CMD ["streamlit", "run", "agent_engine/src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]