import os
from pathlib import Path

from dotenv import load_dotenv

# Explicitly load the .env sitting next to this file, rather than relying
# on python-dotenv's default behavior of searching the current working
# directory. That default breaks depending on how/where the process that
# launches this server (e.g. Claude Desktop) sets its working directory.
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Points at the local FastAPI backend by default. Once deployed, set
# FASTAPI_URL in mcp_server/.env to the cloud URL,
# e.g. https://your-app.onrender.com
FASTAPI_URL = os.getenv("FASTAPI_URL", "https://codeforces-ai-coach.onrender.com")
