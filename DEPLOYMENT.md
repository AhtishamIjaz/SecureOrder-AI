# 🚀 SecureOrder AI - Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Setup](#docker-setup)
3. [Docker Hub Deployment](#docker-hub-deployment)
4. [Hugging Face Spaces Deployment](#hugging-face-spaces-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.11+
- pip/poetry
- OpenAI API Key

### Setup
```bash
# Clone repository
git clone https://github.com/AhtishamIjaz/SecureOrder-AI.git
cd SecureOrder-AI

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Install dependencies
pip install -r requirements.txt
pip install -r agent_engine/requirements.txt
pip install -r mcp_server/requirements.txt

# Run locally
python main.py
```

---

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up --build

# The app will be available at:
# - Streamlit UI: http://localhost:8501
# - MCP Server: http://localhost:8000
```

### Build Individual Images

```bash
# Build main image
docker build -t secureorder-ai:latest .

# Build agent-brain
docker build -f agent_engine/Dockerfile -t secureorder-agent-brain:latest .

# Build mcp-vault
docker build -f mcp_server/Dockerfile -t secureorder-mcp-vault:latest .
```

### Run Standalone

```bash
# Run main container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  secureorder-ai:latest
```

---

## Docker Hub Deployment

### Prerequisites
1. Docker Hub account
2. GitHub secrets configured:
   - `DOCKER_HUB_USERNAME`
   - `DOCKER_HUB_TOKEN`

### Setup GitHub Secrets

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Create new secrets:
   ```
   DOCKER_HUB_USERNAME = your_dockerhub_username
   DOCKER_HUB_TOKEN = your_dockerhub_token
   ```

### How It Works
- On push to `main` or `develop` branch, GitHub Actions automatically:
  1. Builds all Docker images
  2. Tags with `latest` and git SHA
  3. Pushes to Docker Hub

### Pull from Docker Hub
```bash
docker pull username/secureorder-ai:latest
docker pull username/secureorder-agent-brain:latest
docker pull username/secureorder-mcp-vault:latest
```

---

## Hugging Face Spaces Deployment

### Prerequisites
1. Hugging Face account
2. Create new Space at https://huggingface.co/spaces

### Option 1: Direct GitHub Sync
1. Create space: https://huggingface.co/new-space
2. Choose **Docker** as SDK
3. Connect your GitHub repo
4. Select the branch (main)
5. Hugging Face will deploy automatically on push

### Option 2: Manual Setup
```bash
# In your Hugging Face Space repository
git clone https://huggingface.co/spaces/username/secureorder-ai
cd secureorder-ai

# Copy files from your main repo
cp -r ../SecureOrder-AI/* .

# Make sure Dockerfile exists (it will be automatically detected)
# For Hugging Face Spaces, keep the standard Dockerfile

# Git push to Hugging Face
git add .
git commit -m "Deploy SecureOrder AI"
git push
```

### Access Your Space
- URL: `https://huggingface.co/spaces/username/secureorder-ai`
- The app runs automatically with environment handling

---

## CI/CD Pipeline

### GitHub Actions Workflows

#### 1. **Docker Push Workflow** (`.github/workflows/docker-push.yml`)
- Triggers: Push to `main`/`develop`, or PR
- Actions:
  - Builds Docker images
  - Pushes to Docker Hub
  - Updates Docker Hub description

#### 2. **Tests Workflow** (`.github/workflows/tests.yml`)
- Triggers: Push/PR to `main`/`develop`
- Actions:
  - Python linting (flake8)
  - Code formatting check (black)
  - Import sorting (isort)
  - Docker build test

### Enable Workflows

1. Ensure `.github/workflows/` files exist (✅ Done)
2. Set GitHub secrets (Docker Hub credentials)
3. Push to main - workflows automatically run

---

## Troubleshooting

### Issue: "Docker build fails - module not found"

**Solution:**
```bash
# Ensure all requirements.txt files are properly set
pip install -r requirements.txt
pip install -r agent_engine/requirements.txt
pip install -r mcp_server/requirements.txt

# Rebuild
docker-compose up --build
```

### Issue: "OpenAI API Key not recognized"

**Solution:**
```bash
# Verify .env file exists
cp .env.example .env

# Edit and add your actual key
OPENAI_API_KEY=sk-your-actual-key

# For Docker:
docker run -e OPENAI_API_KEY=sk-your-key ...
```

### Issue: "MCP Server connection refused"

**Solution:**
```bash
# Ensure both services are running
docker-compose up --build

# Check logs
docker-compose logs mcp-vault
docker-compose logs agent-brain

# Verify network
docker network ls
docker network inspect secureorder-ai_secureorder-network
```

### Issue: "Port already in use"

**Solution:**
```bash
# Change ports in docker-compose.yml or stop other services
docker-compose down

# Or use different ports
docker run -p 9501:8501 secureorder-ai:latest
```

---

## Environment Variables

Create `.env` file (copy from `.env.example`):

```env
# Required
OPENAI_API_KEY=your_key_here

# Optional (defaults provided)
MCP_SERVER_URL=http://mcp-vault:8000
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
DATABASE_PATH=mcp_server/data/orders.db
ENVIRONMENT=development
DEBUG=false
```

---

## Commands Reference

```bash
# Local
python main.py

# Docker Compose
docker-compose up --build
docker-compose down
docker-compose logs -f

# Docker Build
docker build -t name:tag .
docker push username/name:tag

# GitHub Advanced
git push origin main                    # Triggers CI/CD
git tag v1.0.0 && git push --tags      # Create release
```

---

## Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review logs: `docker-compose logs`
3. Open GitHub Issue: https://github.com/AhtishamIjaz/SecureOrder-AI/issues

---

**Last Updated:** February 2026
