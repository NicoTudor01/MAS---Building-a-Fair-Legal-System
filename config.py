"""
Central configuration for the Fair Legal System MAS.
"""

# ---------------------------------------------------------------------------
# BridgeLLM Proxy (NAT Lab, Tufts)
# Docs: https://github.com/Tufts-University/LLMProxy
# ---------------------------------------------------------------------------
API_KEY = "externalUserBasic-k9t4j4-5ZSqjWJojeedD1VUaB6v1DFMjsEOxezo6CIuKe71"

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
