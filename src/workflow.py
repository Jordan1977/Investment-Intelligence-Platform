from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping


DEFAULT_TARGETS = {
    "prudent": {"Equity": 0.25, "Bonds": 0.45, "Real Estate": 0.10, "Alternative": 0.05, "Cash": 0.15},
    "balanced": {"Equity": 0.50, "Bonds": 0.25, "Real Estate": 0.10, "Alternative": 0.05, "Cash": 0.10},
    "dynamic": {"Equity": 0.70, "Bonds": 0.12, "Real Estate": 0.08, "Alternative": 0.05, "Cash": 0.05},
}


def infer_risk_profile(age: int, horizon_years: int, loss_capacity: str, tolerance: str) -> str:
    """Simple explainable demo rule. Final suitability decision remains human."""
    score = 0
    score += 2 if horizon_years >= 15 else 1 if horizon_years >= 7 else 0
    score += {"low": 0, "medium": 1, "high": 2}.get(loss_capacity, 1)
    score += {"low": 0, "medium": 1, "high": 2}.get(tolerance, 1)
    if age >= 65:
        score -= 1
    if score >= 5:
        return "dynamic"
    if score >= 3:
        return "balanced"
    return "prudent"


def target_allocation(profile: str, liquidity_need_ratio: float = 0.0) -> Dict[str, float]:
    target = dict(DEFAULT_TARGETS.get(profile, DEFAULT_TARGETS["balanced"]))
    # If a meaningful near-term liquidity need exists, increase cash transparently.
    if liquidity_need_ratio > target["Cash"]:
        extra = min(0.20, liquidity_need_ratio - target["Cash"])
        target["Cash"] += extra
        # Reduce risk assets first, then bonds if necessary.
        reduce_equity = min(extra, max(0.0, target["Equity"] - 0.15))
        target["Equity"] -= reduce_equity
        remainder = extra - reduce_equity
        if remainder > 0:
            target["Bonds"] = max(0.0, target["Bonds"] - remainder)
    total = sum(target.values())
    return {k: v / total for k, v in target.items()}


def audit_client(client: Mapping[str, float | int | str]) -> List[Dict[str, str]]:
    alerts: List[Dict[str, str]] = []
    financial = float(client.get("financial_assets", 0) or 0)
    real_estate = float(client.get("real_estate", 0) or 0)
    cash = float(client.get("cash", 0) or 0)
    debt = float(client.get("debt", 0) or 0)
    total = max(financial + real_estate + cash - debt, 1.0)
    if real_estate / total > 0.60:
        alerts.append({"level": "warning", "title": "Concentration immobilière", "text": "Le patrimoine net est fortement concentré en immobilier."})
    if cash / total > 0.20:
        alerts.append({"level": "info", "title": "Liquidités importantes", "text": "Une part significative du patrimoine reste en liquidités ; vérifier le besoin de sécurité et les projets à court terme."})
    horizon = int(client.get("horizon_years", 0) or 0)
    if horizon >= 15 and str(client.get("risk_tolerance", "medium")) == "high":
        alerts.append({"level": "positive", "title": "Horizon long", "text": "L'horizon et la tolérance au risque permettent d'étudier une poche d'actifs de croissance plus importante."})
    if not alerts:
        alerts.append({"level": "positive", "title": "Profil sans anomalie majeure", "text": "Aucune alerte simple n'a été détectée ; l'analyse détaillée du portefeuille reste nécessaire."})
    return alerts


def weighted_score(metrics: Mapping[str, float], weights: Mapping[str, float]) -> float:
    usable = [(k, float(v)) for k, v in weights.items() if k in metrics and metrics[k] is not None]
    denom = sum(w for _, w in usable)
    if denom <= 0:
        return 0.0
    # Metrics are expected to already be normalized 0..100.
    return sum(float(metrics[k]) * w for k, w in usable) / denom
