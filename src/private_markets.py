from __future__ import annotations
import pandas as pd

def private_market_snapshot(universe):
    pe = universe[universe["vehicle"] == "Private Equity"].copy()
    scpi = universe[universe["vehicle"] == "SCPI"].copy()

    pe_rows = []
    for _, r in pe.iterrows():
        rvpi = None
        if pd.notna(r.get("tvpi")) and pd.notna(r.get("dpi")):
            rvpi = float(r["tvpi"] - r["dpi"])
        pe_rows.append({
            "name": r["name"], "irr": float(r["irr"]) if pd.notna(r.get("irr")) else None,
            "tvpi": float(r["tvpi"]) if pd.notna(r.get("tvpi")) else None,
            "dpi": float(r["dpi"]) if pd.notna(r.get("dpi")) else None,
            "rvpi": rvpi, "vintage": int(r["vintage"]) if pd.notna(r.get("vintage")) else None,
            "strategy": r.get("strategy"), "aum_m": float(r["aum_m"]) if pd.notna(r.get("aum_m")) else None
        })

    scpi_rows = []
    for _, r in scpi.iterrows():
        scpi_rows.append({
            "name": r["name"],
            "distribution_rate": float(r["distribution_rate"]) if pd.notna(r.get("distribution_rate")) else None,
            "occupancy_rate": float(r["occupancy_rate"]) if pd.notna(r.get("occupancy_rate")) else None,
            "aum_m": float(r["aum_m"]) if pd.notna(r.get("aum_m")) else None,
            "ter": float(r["ter"]) if pd.notna(r.get("ter")) else None,
        })
    return {"private_equity": pe_rows, "scpi": scpi_rows}
