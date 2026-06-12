def check_missing_prices(items):
    missing = []

    for item in items:
        if not item.get("unit_price"):
            missing.append({
                "name": item["name"],
                "quantity": item.get("quantity")
            })

    return missing