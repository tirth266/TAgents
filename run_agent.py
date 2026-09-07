import os
import json
from datetime import datetime, timezone

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


# ============================================================
# CONFIGURATION
# ============================================================

# Groq API key is supplied by GitHub Actions.
# Never hard-code the API key in this file.
os.environ["GROQ_API_KEY"] = os.environ["SECRET_GROQ_KEY"]

# Use Groq as the LLM provider.
config = DEFAULT_CONFIG.copy()

config["llm_provider"] = "groq"

# Keep the first automated test lightweight.
config["max_debate_rounds"] = 1

config["deep_think_llm"] = os.getenv(
    "TRADINGAGENTS_DEEP_THINK_LLM",
    "groq/compound"
)

config["quick_think_llm"] = os.getenv(
    "TRADINGAGENTS_QUICK_THINK_LLM",
    "groq/compound"
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


# ============================================================
# VALIDATE DECISION
# ============================================================

decision_text = str(decision).strip().upper()

allowed_decisions = {"BUY", "SELL", "HOLD"}

if decision_text not in allowed_decisions:
    raise ValueError(
        f"Unexpected TradingAgents decision: {decision!r}. "
        f"Expected one of: {sorted(allowed_decisions)}"
    )


# ============================================================
# SAVE MACHINE-READABLE DECISION
# ============================================================

decision_record = {
    "symbol": TICKER,
    "analysis_date": analysis_date,
    "decision": decision_text,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
}

with open("decision.json", "w", encoding="utf-8") as f:
    json.dump(decision_record, f, indent=2)


print("\n" + "=" * 70)
print("📄 DECISION FILE CREATED")
print("=" * 70)

print(json.dumps(decision_record, indent=2))

print("\nDecision saved to: decision.json")

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETED")
print("=" * 70)
