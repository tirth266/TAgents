import os
import json
from datetime import datetime, timezone

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


# ============================================================
# CONFIGURATION
# ============================================================

TICKER = "BTC-USD"

analysis_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ============================================================
# PROVIDER FALLBACK ORDER
# ============================================================

PROVIDERS = [
    {
        "name": "Gemini",
        "provider": "google",
        "deep_model": "gemini-3.1-flash-lite",
        "quick_model": "gemini-3.1-flash-lite",
    },
    {
        "name": "Groq",
        "provider": "groq",
        "deep_model": "openai/gpt-oss-120b",
        "quick_model": "openai/gpt-oss-120b",
    },
    {
        "name": "NVIDIA",
        "provider": "nvidia",
        "deep_model": "nvidia/nemotron-3-super-120b-a12b",
        "quick_model": "nvidia/nemotron-3-super-120b-a12b",
    },
]


# ============================================================
# COMMON CONFIGURATION
# ============================================================

base_config = DEFAULT_CONFIG.copy()

# Keep the automated analysis lightweight.
base_config["max_debate_rounds"] = 1

# Keep risk discussion lightweight.
base_config["max_risk_discuss_rounds"] = 1


# ============================================================
# DISPLAY
# ============================================================

print("=" * 70)
print("TRADINGAGENTS AUTOMATED MARKET ANALYSIS")
print("=" * 70)

print(f"Ticker:        {TICKER}")
print(f"Analysis date: {analysis_date}")

print("\nProvider fallback order:")

for index, provider in enumerate(PROVIDERS, start=1):
    print(
        f"{index}. {provider['name']} "
        f"({provider['deep_model']})"
    )

print("=" * 70)


# ============================================================
# RUN WITH PROVIDER FALLBACK
# ============================================================

state = None
decision = None
successful_provider = None
last_error = None


for provider in PROVIDERS:

    print("\n" + "=" * 70)
    print(f"🔄 TRYING PROVIDER: {provider['name']}")
    print("=" * 70)

    print(f"Provider:    {provider['provider']}")
    print(f"Deep model:  {provider['deep_model']}")
    print(f"Quick model: {provider['quick_model']}")

    config = base_config.copy()

    config["llm_provider"] = provider["provider"]

    config["deep_think_llm"] = provider["deep_model"]
    config["quick_think_llm"] = provider["quick_model"]

    # NVIDIA uses its own provider-specific endpoint,
    # so no backend_url override is required here.
    #
    # Gemini uses Google's native client.
    # Groq uses TradingAgents' native Groq provider.
    # NVIDIA uses TradingAgents' native NVIDIA provider.

    try:

        print(
            f"\n🚀 Starting TradingAgents with "
            f"{provider['name']}...\n"
        )

        ta = TradingAgentsGraph(
            debug=True,
            config=config
        )

        print(
            f"📊 Running {TICKER} analysis "
            f"using {provider['name']}..."
        )

        state, decision = ta.propagate(
            TICKER,
            analysis_date
        )

        successful_provider = provider

        print("\n" + "=" * 70)
        print(
            f"✅ SUCCESS — {provider['name']} "
            f"completed the analysis"
        )
        print("=" * 70)

        break

    except Exception as exc:

        last_error = exc

        print("\n" + "=" * 70)
        print(
            f"❌ {provider['name']} FAILED"
        )
        print("=" * 70)

        print(f"Error type: {type(exc).__name__}")
        print(f"Error: {exc}")

        print(
            "\n➡️ Moving to the next provider..."
        )


# ============================================================
# ALL PROVIDERS FAILED
# ============================================================

if successful_provider is None:

    print("\n" + "=" * 70)
    print("❌ ALL LLM PROVIDERS FAILED")
    print("=" * 70)

    raise RuntimeError(
        "Gemini, Groq, and NVIDIA all failed. "
        f"Last error: {last_error}"
    )


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("🎯 TRADINGAGENTS FINAL DECISION")
print("=" * 70)

print(f"Provider used: {successful_provider['name']}")
print(f"Model used:    {successful_provider['deep_model']}")
print(f"Decision:      {decision}")


# ============================================================
# VALIDATE DECISION
# ============================================================

decision_text = str(decision).strip().upper()

allowed_decisions = {
    "BUY",
    "SELL",
    "HOLD"
}

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
    "provider": successful_provider["name"],
    "model": successful_provider["deep_model"],
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
}


with open(
    "decision.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        decision_record,
        f,
        indent=2
    )


# ============================================================
# DISPLAY DECISION FILE
# ============================================================

print("\n" + "=" * 70)
print("📄 DECISION FILE CREATED")
print("=" * 70)

print(
    json.dumps(
        decision_record,
        indent=2
    )
)

print("\nDecision saved to: decision.json")


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 70)
print("✅ ANALYSIS COMPLETED")
print("=" * 70)
