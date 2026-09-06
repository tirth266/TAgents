import os
from datetime import datetime, timezone

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


# ============================================================
# CONFIGURATION
# ============================================================

# Gemini API key is supplied by GitHub Actions.
# Never hard-code API keys in this file.
os.environ["GOOGLE_API_KEY"] = os.environ["SECRET_GOOGLE_KEY"]

# Use Google/Gemini as the LLM provider.
config = DEFAULT_CONFIG.copy()

config["llm_provider"] = "google"

# Keep the first automated test lightweight.
config["max_debate_rounds"] = 1

# These are intentionally configurable through environment
# variables so we can change models later without rewriting code.
config["deep_think_llm"] = os.getenv(
    "TRADINGAGENTS_DEEP_THINK_LLM",
    "gemini-3.6-flash"
)

config["quick_think_llm"] = os.getenv(
    "TRADINGAGENTS_QUICK_THINK_LLM",
    "gemini-3.6-flash"
)


# ============================================================
# MARKET
# ============================================================

TICKER = "BTC-USD"

analysis_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

print("=" * 70)
print("TRADINGAGENTS AUTOMATED MARKET ANALYSIS")
print("=" * 70)
print(f"Ticker:         {TICKER}")
print(f"Analysis date:  {analysis_date}")
print(f"LLM provider:   {config['llm_provider']}")
print(f"Deep model:     {config['deep_think_llm']}")
print(f"Quick model:    {config['quick_think_llm']}")
print("=" * 70)


# ============================================================
# START TRADINGAGENTS
# ============================================================

print("\n🚀 Starting TradingAgents...\n")

ta = TradingAgentsGraph(
    debug=True,
    config=config
)


# ============================================================
# RUN ANALYSIS
# ============================================================

state, decision = ta.propagate(
    TICKER,
    analysis_date
)


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("🎯 TRADINGAGENTS FINAL DECISION")
print("=" * 70)

print(decision)

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETED")
print("=" * 70)
