"""Entry filters for the radar: jurisdiction, capital, regulation, offtake, financeability, and priority for the age-35 goal.

Goal by ~35: nearly passive high income. This usually comes from ownership in an asset or company sitting on a real deficit, not from a high salary.

Occupied niches are not discarded. They stay in consideration if there is a realistic structural entry (share in SPV/JV, service layer, smaller offtake, trade finance).

Additional capital paths:
- Family capital can act as bridge (seed / proof-of-concept).
- Bank credit or trade finance can cover part of medium-capital deals.
- Entry into existing teams or companies with growth/ownership potential is valid.

Priority ranking prefers signals where:
- Ownership (equity or asset share) is realistic, even if the core asset is already held by larger players.
- External capital, family bridge, or existing team entry is possible.
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
    "medium": "€50k–500k (small processing, certifications, equipment). Family bridge or bank credit can cover part.",
    "high": "> €500k (plants, heavy logistics, licensing). Usually needs external investor or existing team.",
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
    "medium": "Possible with family offices, trade finance, bank credit, or strategic partners once there is a contract or small proof. Family bridge helps.",
    "easier": "Offtake or asset-backed structure makes it more understandable for private credit, EIFO-type funds, or commodity investors.",
}

PRIORITY_35 = {
    "high": "Ownership realistic + external/family capital possible + can run in parallel with studies (including structural or service entry in occupied niches).",
    "medium": "One or two of the above are true, or clear structural/service/team entry exists even if core asset is occupied.",
    "low": "Mostly salary-like or requires full-time focus and large personal capital early with no clear entry path.",
}


def score_entry(signal: str) -> dict:
    """Rough heuristic. Real decisions need case-by-case review.

    Occupied niches are kept if structural or service entry is plausible.
    Family bridge capital and existing teams lower the effective barrier.
    """
    s = signal.lower()
    capital = "medium"
    regulation = "medium"
    offtake = "medium"
    financeability = "medium"
    ownership = "medium"
    parallel = "medium"
    structural_entry = False
    family_bridge = True  # assumed available as seed/proof
    existing_team_entry = False
    preferred = ["NL", "DK"]

    if any(w in s for w in ["software", "data", "trading", "arbitrage", "service", "verification", "monitoring", "compliance"]):
        capital = "low"
        regulation = "light"
        financeability = "medium"
        ownership = "high"
        parallel = "high"
        structural_entry = True
        existing_team_entry = True
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
        existing_team_entry = True
    if any(w in s for w in ["copper", "steel", "nickel", "lithium", "rare earth", "transformer", "electrical steel"]):
        structural_entry = True
        existing_team_entry = True
        if financeability == "hard":
            financeability = "medium"

    # Family bridge lowers medium-capital barrier
    if capital == "medium" and family_bridge:
        financeability = "easier" if financeability == "medium" else financeability

    # Priority for the age-35 goal
    if ownership == "high" and financeability in ("easier", "medium") and parallel == "high":
        priority_35 = "high"
    elif structural_entry and (ownership in ("high", "medium") or financeability in ("easier", "medium") or existing_team_entry):
        priority_35 = "medium"
    elif ownership == "high" or financeability == "easier" or existing_team_entry:
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
        "family_bridge": family_bridge,
        "existing_team_entry": existing_team_entry,
        "priority_35": priority_35,
        "preferred_jurisdictions": preferred,
        "notes": "Occupied niches kept if structural/service/team entry exists. Family bridge and bank credit lower medium-capital barrier. Priority_35 prefers ownership + capital path + ability to start while studying.",
    }
