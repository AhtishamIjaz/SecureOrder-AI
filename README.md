---
title: SecureOrder AI
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ SecureOrder AI: Industrial Procurement Agent

An enterprise-grade AI system using **Model Context Protocol (MCP)** and **LangGraph** to manage secure inventory and order workflows.

## 🏗️ System Architecture
* **The Vault (MCP Server):** A secure FastMCP server managing a SQLite database with Pydantic validation.
* **The Brain (Agent Engine):** A LangGraph orchestrator with **Human-in-the-Loop** (HITL) safety gates for order approval.
* **The Interface:** A Streamlit dashboard for real-time interaction and order tracking.

## 🛠️ Tech Stack
* **Logic:** Python 3.11, LangGraph, FastMCP
* **Security:** Pydantic V2, GitHub Secrets
* **DevOps:** Docker, GitHub Actions, `uv` package manager

## 🚀 Local Quickstart
If you want to run this locally:
1.  **Install dependencies:**
    ```bash
    uv sync
    ```
2.  **Initialize Database:**
    ```bash
    python mcp_server/src/database.py
    ```
3.  **Run the Agent:**
    ```bash
    uv run streamlit run agent_engine/src/app.py
    ```

## 🔒 Security Note
This project uses **Environment Variables** for API keys. Ensure your `.env` file is never committed to version control (protected by `.gitignore`).