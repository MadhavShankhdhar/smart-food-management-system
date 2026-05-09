def calculate_waste(cooked, consumed):
    waste = cooked - consumed
    waste_pct = (waste / cooked) * 100 if cooked > 0 else 0
    return waste, waste_pct