import os

from dotenv import load_dotenv

load_dotenv()

# Points at the local FastAPI backend by default. Once deployed, set
# FASTAPI_URL in this environment (or the MCP server's env config in
# Claude Desktop) to the cloud URL, e.g. https://your-app.onrender.com
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")
