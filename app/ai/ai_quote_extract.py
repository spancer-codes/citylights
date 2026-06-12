import re


def extract_from_whatsapp(message: str):
    """
    VERY SIMPLE mock extractor (replace with AI later)
    """

    message_lower = message.lower()

    # --- Extract location (simple)
    location = None
    for area in ["harare", "kuwadzana", "avondale", "borrowdale", "chitungwiza"]:
        if area in message_lower:
            location = area.capitalize()

    # --- Extract quantities + items
    pattern = r"(\d+)\s*(lights?|sockets?|plugs?|db box|conduit|wiring)"
    matches = re.findall(pattern, message_lower)

    items = []
    for qty, name, unit_price in matches:
        items.append({
            "name": name,
            "quantity": float(qty),
            "unit_price": float(unit_price) if unit_price else None
        })

    # --- Extract client (very basic assumption: after "for")
    client = None
    if "for" in message_lower:
        parts = message.split("for")
        if len(parts) > 1:
            client = parts[1].split(",")[0].strip()

    return {
        "job_type": "Electrical installation",
        "location": location,
        "client_name": client,
        "items": items
    }