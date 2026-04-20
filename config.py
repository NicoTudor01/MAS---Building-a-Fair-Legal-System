"""
Central configuration for the Fair Legal System MAS.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

# ---------------------------------------------------------------------------
# BridgeLLM Proxy (NAT Lab, Tufts)
# Docs: https://github.com/Tufts-University/LLMProxy
# One key per group member; jurors 1–4 get a dedicated key each.
# Juror 5 is assigned a key randomly at runtime (see main.py).
# ---------------------------------------------------------------------------
API_KEY_LABELS = [
    "LLMPROXY_API_KEY_1",
    "LLMPROXY_API_KEY_2",
    "LLMPROXY_API_KEY_3",
    "LLMPROXY_API_KEY_4",
]

API_KEYS = [os.getenv(label, "") for label in API_KEY_LABELS]

# Available models (default plan):
#   "4o-mini"                                  – OpenAI GPT-4o mini
#   "us.anthropic.claude-3-haiku-20240307-v1:0" – Anthropic Claude 3 Haiku
#   "gemini-2.5-flash-lite"                    – Google Gemini 2.5 Flash Lite
# Use model_info() from LLMProxy to see the full list for your key.
MODEL = "4o-mini"

# ---------------------------------------------------------------------------
# Deliberation settings
# ---------------------------------------------------------------------------
GUILT_THRESHOLD = 0.67   # confidence ≥ this → GUILTY
NUM_JURORS      = 5

# How many prior exchanges to include as context on each LLMProxy call.
# 0 = no history (we manage state manually); increase for longer memory.
LAST_K = 0

# ---------------------------------------------------------------------------
# Voting mechanisms available
# ---------------------------------------------------------------------------
VOTING_METHODS = ["plurality", "social_welfare", "tournament", "slater"]
