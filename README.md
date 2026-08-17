# Investment Intelligence Platform

Professional-grade prototype covering investment selection, portfolio audit, advisory support, client reporting and market monitoring.

The platform is intentionally designed as a **decision layer around tools such as Quantalys / Excel exports**, not as a replacement for them.

## Role coverage

1. **Investment selection** — multi-asset screener, eligibility filters, peer-relative scoring and explainable score decomposition.
2. **Portfolio audit** — allocation, concentration, correlations, drawdown, VaR, risk contribution proxies, cost and diversification diagnostics.
3. **Personalised recommendations** — target allocation by client profile, allocation gaps, candidate supports and rationale.
4. **Client situation report** — automated pedagogical synthesis generated from the same audit data.
5. **Market intelligence** — market regimes, watchlist and opportunity radar.
6. **Continuous improvement** — config-driven scoring, CSV adapters, tests, scheduled GitHub Actions rebuild and GitHub Pages deployment.

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
