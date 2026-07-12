import os

from dotenv import load_dotenv

load_dotenv()

# Codeforces handles to auto-sync on a schedule. Comma-separated in the
# TRACKED_HANDLES env var, e.g. "J_A_I_KUMAR,someoneElse".
TRACKED_HANDLES = [
    h.strip()
    for h in os.getenv("TRACKED_HANDLES", "J_A_I_KUMAR").split(",")
    if h.strip()
]

# How often (in hours) to auto-refresh problems/contests/submissions.
SYNC_INTERVAL_HOURS = int(os.getenv("SYNC_INTERVAL_HOURS", "6"))

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
