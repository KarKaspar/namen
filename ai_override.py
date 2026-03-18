"""
AI Override Module for Window Manufacturing App
================================================
Adds a Mistral-powered interactive CLI to handle irregular/custom calculations
that fall outside the standard CSV rules.
 
Usage:
    python3 ai_override.py                          # interactive mode
    python3 ai_override.py --laius 1200 --kõrgus 900 --query "add 15% curved glass surcharge"
 
Requirements:
    pip install mistralai
"""
 
import argparse
import json
from mistralai import Mistral
from app import WindowManufacturingApp
 
# ── CONFIG ──────────────────────────────────────────────────────────────────
MISTRAL_API_KEY = "Mistral_api"   # <-- paste your key here
MISTRAL_MODEL   = "mistral-small-latest"
CSV_FILE        = "Tootmisreeglid - Sheet1.csv"
# ────────────────────────────────────────────────────────────────────────────
 
 
SYSTEM_PROMPT = """
You are an expert assistant for a window manufacturing calculator.
You receive:
  1. The standard calculated output (JSON) from the app
  2. A user request describing an irregular or custom adjustment
 
Your job:
  - Understand which measurements need to change
  - Apply the requested irregularity (e.g. trapezoidal shape, surcharge %, extra cuts, curved glass)
  - Return ONLY a valid JSON object with:
      {
        "adjustments": {
          "<field_name>": <new_value>,
          ...
        },
        "explanation": "<short human-readable explanation of what was changed and why>"
      }
 
Rules:
  - Only include fields that actually change in "adjustments"
  - All measurement values must be integers (millimeters)
  - Percentages/surcharges should be applied to the relevant field values
  - If the request is unclear, make reasonable assumptions and explain them
  - Never return negative measurements
  - Field names must match exactly: raam_L, raam_H, raam_tk, klaasi_L, klaasi_H, klaasi_tk,
    lengi_UH, lengi_AH, lengi_VERT, raami_UH, raami_AH, raami_VERT, raami_HOR, raami_VERT2,
    klaasiliistud_H, klaasiliistud_VERT
"""
 
 
def run_standard_calc(laius, kõrgus, toote_tyyp, tk, käsi):
    """Run the standard WindowManufacturingApp calculation."""
    app = WindowManufacturingApp(CSV_FILE)
    input_params = {
        'toote tyyp': toote_tyyp,
        'laius': laius,
        'kõrgus': kõrgus,
        'tk tyyptellimusel': tk,
        'käsi': käsi
    }
    return app.calculate_output(input_params)
 
 
def ask_mistral_override(standard_output: dict, user_query: str) -> dict:
    """
    Send standard output + user query to Mistral and get back adjusted values.
    Returns dict with 'adjustments' and 'explanation'.
    """
    client = Mistral(api_key=MISTRAL_API_KEY)
 
    # Filter out None values for cleaner context
    clean_output = {k: v for k, v in standard_output.items() if v is not None}
 
    user_message = f"""
Standard calculation result:
{json.dumps(clean_output, indent=2)}
 
User's irregular request:
{user_query}
"""
 
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ]
    )
 
    raw = response.choices[0].message.content.strip()
 
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
 
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "adjustments": {},
            "explanation": f"Could not parse Mistral response: {raw}"
        }
 
 
def apply_adjustments(standard_output: dict, ai_result: dict) -> dict:
    """Merge AI adjustments on top of standard output."""
    merged = dict(standard_output)
    for field, value in ai_result.get("adjustments", {}).items():
        merged[field] = value
    return merged
 
 
def print_comparison(standard: dict, final: dict, explanation: str):
    """Print a side-by-side diff of standard vs AI-adjusted output."""
    print("\n" + "═" * 60)
    print("  STANDARD  →  AI ADJUSTED")
    print("═" * 60)
 
    changed = False
    for key in final:
        std_val = standard.get(key)
        fin_val = final.get(key)
        if std_val is None and fin_val is None:
            continue
        if std_val != fin_val:
            print(f"  {key:<28} {str(std_val):<10} →  {fin_val}  ✏️")
            changed = True
        else:
            if fin_val is not None:
                print(f"  {key:<28} {fin_val}")
 
    if not changed:
        print("  (no changes applied)")
 
    print("═" * 60)
    print(f"\n🤖 Mistral explanation:\n   {explanation}\n")
 
 
def interactive_mode(laius, kõrgus, toote_tyyp, tk, käsi):
    """Run an interactive loop for multiple AI override queries."""
    print("\n🪟  Window Calculator — AI Override Mode")
    print(f"   Product: {toote_tyyp} | {laius}×{kõrgus}mm | tk={tk} | käsi={käsi}")
    print("   Type your irregular request, or 'exit' to quit.\n")
 
    standard_output = run_standard_calc(laius, kõrgus, toote_tyyp, tk, käsi)
 
    print("Standard calculation:")
    for k, v in standard_output.items():
        if v is not None:
            print(f"  {k}: {v}")
 
    while True:
        print()
        query = input("📐 Irregular request: ").strip()
        if query.lower() in ("exit", "quit", "q"):
            print("Bye! 👋")
            break
        if not query:
            continue
 
        print("⏳ Asking Mistral...")
        ai_result = ask_mistral_override(standard_output, query)
        final_output = apply_adjustments(standard_output, ai_result)
        print_comparison(standard_output, final_output, ai_result.get("explanation", ""))
 
        save = input("💾 Save adjusted result to output.json? (y/N): ").strip().lower()
        if save == "y":
            with open("output.json", "w") as f:
                json.dump({
                    "input": {
                        "toote_tyyp": toote_tyyp,
                        "laius": laius,
                        "kõrgus": kõrgus,
                        "tk": tk,
                        "käsi": käsi
                    },
                    "query": query,
                    "standard_output": standard_output,
                    "ai_adjustments": ai_result.get("adjustments", {}),
                    "explanation": ai_result.get("explanation", ""),
                    "final_output": final_output
                }, f, indent=2)
            print("   Saved to output.json ✅")
 
 
# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Window Calculator — AI Override Mode")
    parser.add_argument("--toote-tyyp",          type=str, default="40STAND60x63")
    parser.add_argument("--laius",               type=int, default=900)
    parser.add_argument("--kõrgus",              type=int, default=900)
    parser.add_argument("--tk-tyyptellimusel",   type=int, default=3)
    parser.add_argument("--käsi",                type=str, default="P")
    parser.add_argument("--query",               type=str, default=None,
                        help="One-shot query (non-interactive). E.g. 'add 15%% surcharge for curved glass'")
    args = parser.parse_args()
 
    if args.query:
        # One-shot mode
        standard = run_standard_calc(args.laius, args.kõrgus, args.toote_tyyp,
                                     args.tk_tyyptellimusel, args.käsi)
        ai_result = ask_mistral_override(standard, args.query)
        final = apply_adjustments(standard, ai_result)
        print_comparison(standard, final, ai_result.get("explanation", ""))
    else:
        # Interactive loop
        interactive_mode(
            laius      = args.laius,
            kõrgus     = args.kõrgus,
            toote_tyyp = args.toote_tyyp,
            tk         = args.tk_tyyptellimusel,
            käsi       = args.käsi
        )
 
