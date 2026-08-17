from __future__ import annotations
import math

def structured_scenarios(row: dict) -> dict:
    coupon = float(row.get("coupon") or 0.0)
    barrier_level = float(row.get("barrier") or 0.60)
    autocall = str(row.get("autocall") or "").lower().startswith("oui")

    scenarios = []
    for label, perf in [
        ("Hausse forte", 0.25), ("Hausse modérée", 0.08), ("Stable", 0.00),
        ("Baisse modérée", -0.20), ("Proche barrière", barrier_level-1+0.02),
        ("Sous barrière", barrier_level-1-0.12),
    ]:
        if perf >= 0:
            product_return = coupon if coupon else perf
            event = "Rappel possible" if autocall else "Coupon / participation"
        elif perf > barrier_level-1:
            product_return = 0.0
            event = "Capital préservé à maturité (illustratif)"
        else:
            product_return = perf
            event = "Perte en capital"
        scenarios.append({
            "label": label, "underlying_return": perf,
            "product_return": float(product_return), "event": event
        })
    distance_to_barrier = 1.0 - barrier_level
    return {
        "coupon": coupon, "barrier": barrier_level, "autocall": autocall,
        "distance_to_barrier": distance_to_barrier, "scenarios": scenarios
    }
