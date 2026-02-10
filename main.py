import subprocess
import sys

if __name__ == "__main__":
    # Run the Streamlit app from agent_engine
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "agent_engine/src/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])
