from __future__ import annotations

def suitability_assessment(audit: dict, current: dict, profile: dict) -> dict:
    target = profile["target"]
    gap = sum(abs(float(current.get(k, 0)) - float(target.get(k, 0))) for k in set(current) | set(target)) / 2
    allocation_fit = max(0.0, 100.0 * (1.0 - gap))

    vol = float(audit.get("metrics", {}).get("volatility") or 0.0)
    risk_budget = float(profile.get("risk_budget", 0.15))
    risk_fit = 100.0 if vol <= risk_budget else max(0.0, 100.0 * (1 - (vol-risk_budget)/max(risk_budget, 0.01)))

    liq = float(audit.get("liquidity_score") or 0.0)
    cost = float(audit.get("cost_score") or 0.0)
    div = float(audit.get("diversification_score") or 0.0)

    score = 0.40*allocation_fit + 0.25*risk_fit + 0.15*liq + 0.10*cost + 0.10*div
    status = "Compatible" if score >= 80 else "À ajuster" if score >= 60 else "Inadapté"

    reasons = []
    if allocation_fit < 75:
        reasons.append("allocation éloignée du profil cible")
    if risk_fit < 75:
        reasons.append("risque historique supérieur au budget indicatif")
    if liq < 60:
        reasons.append("liquidité limitée")
    if cost < 60:
        reasons.append("coûts relativement élevés")
    if not reasons:
        reasons.append("allocation et risque globalement cohérents avec le profil")

    return {
        "score": float(score),
        "status": status,
        "allocation_fit": float(allocation_fit),
        "risk_fit": float(risk_fit),
        "liquidity_fit": liq,
        "cost_fit": cost,
        "diversification_fit": div,
        "reasons": reasons,
    }
