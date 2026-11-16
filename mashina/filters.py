"""Entry filters for the radar: jurisdiction, capital, regulation, offtake, financeability, and priority for the age-35 goal.

Goal by ~35: nearly passive high income. This usually comes from ownership in an asset or company sitting on a real deficit, not from a high salary.

Occupied niches are not discarded. They stay in consideration if there is a realistic structural entry (share in SPV/JV, service layer, smaller offtake, trade finance).

Priority ranking prefers signals where:
- Ownership (equity or asset share) is realistic, even if the core asset is already held by larger players.
- External capital can be brought in relatively early.
- The project can be started in parallel with studies, not instead of them.
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

PRIORITY_35 = {
    "high": "Ownership realistic + external capital possible + can run in parallel with studies (including structural or service entry in occupied niches).",
    "medium": "One or two of the above are true, or clear structural/service entry exists even if core asset is occupied.",
    "low": "Mostly salary-like or requires full-time focus and large personal capital early with no clear entry path.",
}


def score_entry(signal: str) -> dict:
    """Rough heuristic. Real decisions need case-by-case review.

    Occupied niches are kept if structural or service entry is plausible.
    """
    s = signal.lower()
    capital = "medium"
    regulation = "medium"
    offtake = "medium"
    financeability = "medium"
    ownership = "medium"
    parallel = "medium"
    structural_entry = False
    preferred = ["NL", "DK"]

    if any(w in s for w in ["software", "data", "trading", "arbitrage", "service", "verification", "monitoring", "compliance"]):
        capital = "low"
        regulation = "light"
        financeability = "medium"
        ownership = "high"
        parallel = "high"
        structural_entry = True
    if any(w in s for w in ["refining", "processing", "plant", "mine", "smelter"]):
        capital = "high"
        regulation = "heavy"
        financeability = "hard"
        ownership = "high"
        parallel = "low"
    if any(w in s for w in ["defense", "pharma", "energy infrastructure", "nuclear"]):
        regulation = "heavy"
        capital = "high"
        financeability = "hard"
        ownership = "medium"
        parallel = "low"
    if any(w in s for w in ["cbam", "green", "renewable", "tender", "public", "offtake"]):
        offtake = "strong"
        financeability = "easier"
        ownership = "high"
        structural_entry = True
    if any(w in s for w in ["copper", "steel", "nickel", "lithium", "rare earth", "transformer", "electrical steel"]):
        # Occupied industrial niches still get structural entry credit
        structural_entry = True
        if financeability == "hard":
            financeability = "medium"

    # Priority for the age-35 goal, including occupied niches with entry paths
    if ownership == "high" and financeability in ("easier", "medium") and parallel == "high":
        priority_35 = "high"
    elif structural_entry and (ownership in ("high", "medium") or financeability in ("easier", "medium")):
        priority_35 = "medium"
    elif ownership == "high" or financeability == "easier":
        priority_35 = "medium"
    else:
        priority_35 = "low"

    return {
        "capital": capital,
        "regulation": regulation,
        "offtake": offtake,
        "financeability": financeability,
        "ownership": ownership,
        "parallel_with_studies": parallel,
        "structural_entry": structural_entry,
        "priority_35": priority_35,
        "preferred_jurisdictions": preferred,
        "notes": "Occupied niches are kept when structural or service entry is realistic. Priority_35 prefers ownership + external capital + ability to start while studying.",
    }
