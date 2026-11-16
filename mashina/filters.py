"""Entry filters for the radar: jurisdiction, capital barrier, regulation, offtake, and external financeability.

These filters turn a price signal into actionable questions:
1. Can I enter this with limited personal capital?
2. Can external investors be brought in?
3. Where does this make the most sense jurisdictionally?
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

FINANCEABILITY = {
    "hard": "Mostly personal capital or very patient angels. Needs strong track record or unique access.",
    "medium": "Possible with family offices, trade finance, or strategic partners once there is a contract or small proof.",
    "easier": "Offtake or asset-backed structure makes it more understandable for private credit, EIFO-type funds, or commodity investors.",
}


def score_entry(signal: str) -> dict:
    """Rough heuristic. Real decisions need case-by-case review."""
    s = signal.lower()
    capital = "medium"
    regulation = "medium"
    offtake = "medium"
    financeability = "medium"
    preferred = ["NL", "DK"]

    if any(w in s for w in ["software", "data", "trading", "arbitrage", "service"]):
        capital = "low"
        regulation = "light"
        financeability = "medium"
    if any(w in s for w in ["refining", "processing", "plant", "mine", "smelter"]):
        capital = "high"
        regulation = "heavy"
        financeability = "hard"
    if any(w in s for w in ["defense", "pharma", "energy infrastructure", "nuclear"]):
        regulation = "heavy"
        capital = "high"
        financeability = "hard"
    if any(w in s for w in ["cbam", "green", "renewable", "tender", "public", "offtake"]):
        offtake = "strong"
        financeability = "easier"

    return {
        "capital": capital,
        "regulation": regulation,
        "offtake": offtake,
        "financeability": financeability,
        "preferred_jurisdictions": preferred,
        "notes": "Heuristic only. Strong offtake improves external financeability the most.",
    }
