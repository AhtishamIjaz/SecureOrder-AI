#!/bin/bash
# Debug script to verify Docker builds locally

echo "=== Testing Local Docker Build ==="
echo ""

# Test main Dockerfile
echo "1. Building main Dockerfile..."
docker build -f ./Dockerfile -t secureorder-ai:test . 2>&1 | tail -20
echo "✓ Main Dockerfile built successfully"
echo ""

# Test agent-brain Dockerfile
echo "2. Building agent_engine Dockerfile..."
docker build -f ./agent_engine/Dockerfile -t secureorder-agent-brain:test . 2>&1 | tail -20
echo "✓ Agent Dockerfile built successfully"
echo ""

# Test mcp-vault Dockerfile
echo "3. Building mcp_server Dockerfile..."
docker build -f ./mcp_server/Dockerfile -t secureorder-mcp-vault:test . 2>&1 | tail -20
echo "✓ MCP Dockerfile built successfully"
echo ""

echo "=== Build Test Complete ==="
echo ""
echo "Next steps:"
echo "1. Verify GitHub Actions secrets are set:"
echo "   - DOCKER_HUB_USERNAME"
echo "   - DOCKER_HUB_TOKEN"
echo ""
echo "2. Check GitHub Actions at: https://github.com/AhtishamIjaz/SecureOrder-AI/actions"
echo ""
echo "3. For Hugging Face:"
echo "   - Go to https://huggingface.co/spaces"
echo "   - Create a new Docker space"
echo "   - Connect to your GitHub repo"
echo "   - Select main branch"
echo "   - Rebuild/rebuild-without-cache"
