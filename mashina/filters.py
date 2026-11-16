"""Entry filters for the radar: jurisdiction, capital barrier, regulation, offtake.

These filters turn a price signal into a question the user can actually act on:
"Can I enter this with limited capital, outside or inside Denmark?"

They are deliberately coarse and public. They do not try to be complete.
"""

JURISDICTIONS = {
    "DK": {"tax": "high", "speed": "medium", "notes": "Good for living and EU access, expensive to operate."},
    "NL": {"tax": "medium", "speed": "fast", "notes": "Strong commodity and logistics hub."},
    "CH": {"tax": "low", "speed": "medium", "notes": "Trading and holding companies."},
    "SG": {"tax": "low", "speed": "fast", "notes": "Asia trading and finance."},
    "AE": {"tax": "low", "speed": "fast", "notes": "Energy and commodity trading."},
    "US": {"tax": "medium", "speed": "medium", "notes": "Large market, complex regulation."},
}

CAPITAL_BARRIERS = {
    "low": "Can start with < €50k (trading, software, light services).",
    "medium": "€50k–500k (small processing, certifications, equipment).",
    "high": "> €500k (plants, heavy logistics, licensing).",
}

REGULATION = {
    "light": "Mostly commercial contracts and standard product rules.",
    "medium": "Industry standards, some permits, or REACH/CBAM-type rules.",
    "heavy": "Licensing, environmental permits, defense, pharma, or energy infrastructure.",
}

OFFTAKE = {
    "weak": "No obvious obligated buyer.",
    "medium": "Large industrial buyers exist, but no hard obligation.",
    "strong": "Public tenders, long-term offtake agreements, or mandated demand (e.g. green targets).",
}


def score_entry(signal: str) -> dict:
    """Very rough heuristic. Real scoring needs manual review of the specific case."""
    s = signal.lower()
    capital = "medium"
    regulation = "medium"
    offtake = "medium"
    preferred = ["NL", "DK"]

    if any(w in s for w in ["software", "data", "trading", "arbitrage", "service"]):
        capital = "low"
        regulation = "light"
    if any(w in s for w in ["refining", "processing", "plant", "mine", "smelter"]):
        capital = "high"
        regulation = "heavy"
    if any(w in s for w in ["defense", "pharma", "energy infrastructure", "nuclear"]):
        regulation = "heavy"
        capital = "high"
    if any(w in s for w in ["cbam", "green", "renewable", "tender", "public"]):
        offtake = "strong"

    return {
        "capital": capital,
        "regulation": regulation,
        "offtake": offtake,
        "preferred_jurisdictions": preferred,
        "notes": "Heuristic only. Check offtake and permits before acting.",
    }
