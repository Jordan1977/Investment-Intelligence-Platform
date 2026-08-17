# Investment Intelligence Platform

Professional-grade prototype covering investment selection, portfolio audit, advisory support, client reporting and market monitoring.

The platform is intentionally designed as a **decision layer around tools such as Quantalys / Excel exports**, not as a replacement for them.

## Role coverage

1. **Guided walkthrough** — a "Parcours complet" tab runs a fictitious client end-to-end through the whole pipeline (portfolio import → diagnosis → recommendation → report) in one narrative, data-driven page.
2. **Investment selection** — multi-asset screener (36 instruments across Equity, Bonds, Alternative, Real Estate), eligibility filters, peer-relative scoring and explainable score decomposition.
3. **Asset-class-specific analysis** — dedicated fact sheets for Private Equity (IRR, TVPI, DPI, vintage, strategy), SCPI (distribution rate, occupancy rate) and structured products (coupon, barrier, autocall, illustrative payoff diagram), in addition to the standard listed-fund analytics (performance, drawdown, rolling Sharpe).
4. **Portfolio audit** — allocation, concentration, correlations, drawdown, VaR, risk contribution proxies, cost and diversification diagnostics, with a threshold-based alert engine.
5. **Personalised recommendations** — target allocation by client profile, allocation gaps, candidate supports and rationale.
6. **Client situation report** — automated pedagogical synthesis generated from the same audit data, exportable as a print-ready PDF (browser print, formatted via a dedicated print stylesheet).
7. **Market intelligence** — market regimes, watchlist and opportunity radar.
8. **Continuous improvement** — config-driven scoring, CSV adapters, tests, scheduled GitHub Actions rebuild and GitHub Pages deployment.


## V10 Interview Edition

V10 adds the modules that make the prototype closer to an actual investment-committee workflow:

- **Portfolio Stress Lab** — equity shock, rate shock, credit widening, FX shock and global risk-off scenarios.
- **Fund Overlap Engine** — semi-quantitative overlap based on benchmark, category, geography, sector and correlation.
- **Client Suitability Matrix** — allocation fit, risk-budget fit, liquidity, cost and diversification by client profile.
- **Investment Committee Book** — Approved / Watch / Review / Reject status with a documented rationale.
- **Structured Products Lab** — scenario table, barrier distance and illustrative product-return outcomes.
- **Private Markets Lab** — IRR / TVPI / DPI / RVPI peer view and SCPI distribution / occupancy comparison.
- **Data Quality Monitor** — completeness and duplicate checks on the imported universe.
- **Audit trail logic** — every ranking, committee status and suitability conclusion is explainable from stored metrics/rules.

The V10 objective is not to add decorative features. Each module answers a decision question used during portfolio review or investment selection.

## Run locally

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py --demo
python -m http.server 8000 -d docs
```

Open `http://localhost:8000`.

For live listed-market data:

```bash
python scripts/build_site.py --live
```

If the live provider is unavailable, the build automatically falls back to deterministic demo data so the dashboard remains usable.

## Quantalys / Excel workflow

```text
Quantalys / Excel / API
        ↓
CSV export / standardisation
        ↓
Python analytical layer
        ↓
Screening / Portfolio X-Ray / Advisory / Reporting
        ↓
GitHub Pages dashboard
```

`src/data_loader.py` contains common French/English column aliases to simplify adaptation of exports.

## Important

All client portfolio data in this repository is fictitious. Scores are illustrative and must be calibrated to the firm's process. The platform is decision support only and does not provide regulated investment advice.
