def ask_ai(query: str) -> str:
    if "humalyzer" in query.lower():
        return "The Humalyzer is a semi-automated biochemistry analyzer."
    elif "humacount" in query.lower():
        return "The HumaCount is a hematology analyzer for blood analysis."
    return "Sorry, I don't have enough information to answer that."
