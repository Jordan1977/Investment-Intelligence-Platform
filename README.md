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


## V12 — Finition métier (en cours)

Cahier des charges V12 : 22 priorités visant une démonstration "impressionnante non par le nombre de graphiques mais par la cohérence de son raisonnement de bout en bout", avec pour exigence centrale que **le dossier client influence véritablement toutes les étapes suivantes**.

Compte tenu de l'ampleur du cahier des charges, cette itération traite en profondeur les 3 priorités que le cahier des charges qualifie lui-même de changement majeur, plus la validation de données (peu coûteuse, très rentable en crédibilité) :

### Priorité 1 — Financial & Patrimonial Diagnostic Engine
Le moteur ne se limite plus à âge/horizon/tolérance/capacité de perte. Nouveaux champs client (patrimoine professionnel, autres actifs, mensualités de crédit) et calculs réels :
- Patrimoine brut, patrimoine net, composition par poste (financier / immobilier / professionnel / liquidités / autres).
- Endettement : dette/brut, dette/net, taux d'effort approximatif — alertes explicables (« endettement significatif » / « modéré »), jamais de conclusion réglementaire automatique.
- Épargne de précaution en mois de dépenses, plage indicative 3–6 mois affichée sans être imposée comme règle universelle.
- Taux d'épargne, capacité mensuelle/annuelle.
- Concentration patrimoniale avec diagnostics du type « 72 % du patrimoine net est immobilier » — jamais de recommandation d'action directe (« il faut vendre »).

### Priorité 2 — Goal-based investing / compartiments
Changement structurel : le capital n'est plus traité de façon uniforme selon le seul profil. Chaque objectif est rattaché à un compartiment (Sécurité 0–3 ans, Projets moyen terme 3–8 ans, Croissance long terme 8 ans+, Transmission) selon son horizon. **Point de rigueur traité explicitement** : un objectif à long terme (ex. retraite dans 25 ans, 400 k€) porte un montant *cible futur*, pas du capital à isoler aujourd'hui — contrairement à un objectif à 3–8 ans, où le montant cible est assimilé au besoin de capital présent. Le compartiment long terme reçoit le capital résiduel, pas la somme brute des objectifs.

### Priorité 3 — Allocation stratégique par compartiments
L'allocation proposée résulte désormais de la pondération des compartiments (et non plus seulement d'une grille profil → allocation). L'analyste dispose toujours d'une allocation strategique proposée qu'il peut entièrement modifier, avec un bouton dédié pour revenir à la proposition recalculée sans perdre ses propres ajustements par erreur. Les textes « Pourquoi cette allocation ? » sont générés à partir des données réelles du dossier (horizon, part de l'enveloppe en long terme, concentration immobilière effective, etc.) — plus de texte générique identique d'un client à l'autre.

### Priorité 20 — Validation des données
Âge (18–100), horizon (> 0), montants négatifs, horizon d'objectif nul : rejetés avec un message clair avant toute analyse, plutôt que de produire un calcul silencieusement faux.

### Priorité 18 — Cohérence des données (testée explicitement)
Un test automatisé change l'âge et le profil de risque d'un dossier déjà analysé et vérifie que le profil synthétique, l'allocation stratégique et les textes explicatifs changent réellement en conséquence — pas de texte résiduel de l'ancien cas.

### Priorité 4 — Portfolio Diagnostic complet (11 blocs)
L'audit du portefeuille détenu couvre désormais allocation, enveloppes, géographie, secteurs, devises, liquidité (classification Très liquide/Liquide/Moins liquide/Illiquide), frais, risque (volatilité estimée), concentration (plus grande ligne), overlap et adéquation aux objectifs. Toutes les alertes affichent un niveau de sévérité **CRITICAL / WARNING / INFO**, avec un exemple correspondant exactement au cahier des charges : un besoin de capital à court terme (compartiment Sécurité) mal couvert par la poche cash/obligataire du portefeuille détenu déclenche une alerte CRITICAL "Adéquation aux objectifs".

### Priorité 6 — Scoring transparent (Quality / Client Fit / House View)
Le score n'est plus une note unique. Chaque support affiche trois notes distinctes — **Product Quality Score** (qualité intrinsèque par méthodologie différenciée), **Client Fit Score** (adéquation au dossier), **House View** (conviction tactique du comité) — combinées via une formule finale explicite et configurable (60/30/10 par défaut, réglable dans Investment Policy). Un bouton "Détail du score" affiche la formule appliquée et la contribution de chaque critère individuel au Quality Score (écart à une note neutre de 50/100).

### Priorité 8 — Client Fit approfondi
Le Client Fit intègre désormais le niveau de risque, l'horizon, l'illiquidité du support rapportée à l'horizon client, l'expérience financière, le besoin de liquidité à court terme (croisé avec les compartiments de la Priorité 2), la diversification apportée et le besoin de revenus. Cas explicitement géré : un support à Quality élevée (≥ 78) mais Client Fit faible (< 45) reçoit la mention **"Produit de qualité mais non adapté à ce dossier"**.

### Priorité 9 — Before/After Premium
Nouvelle comparaison Current Portfolio vs Proposed Portfolio sur coûts, volatilité estimée, concentration (plus grande ligne) et diversification (indice de Herfindahl, même méthodologie appliquée aux deux portefeuilles pour une comparaison rigoureuse). Section **"What changed?"** (deltas par classe d'actifs et par métrique) suivie de **"Why?"**, qui relie chaque changement notable à un constat précis identifié lors de l'audit du portefeuille détenu (ex. une baisse de la poche actions est reliée au constat "Exposition actions élevée" relevé à l'audit).

### Bug corrigé pendant cette itération
Les champs numériques absents d'un import CSV (ex. Sharpe non applicable à un fonds Private Equity) étaient convertis en `0` et traités comme une valeur réelle dans le classement percentile, au lieu d'être exclus — un fonds Private Equity pouvait ainsi recevoir la mention incohérente "Sharpe favorable". Corrigé partout (10 occurrences) via une fonction `isNumericValue()` dédiée, avec un test de non-régression associé.

### Priorité 5 — Mapping CSV visuel
À l'import d'un CSV Quantalys externe (hors recherches de démonstration, déjà au bon format), l'outil détecte automatiquement les colonnes reconnues et affiche un tableau "Colonne détectée → Mappée vers" avec le taux de reconnaissance — matérialisant concrètement le principe "Quantalys-compatible / adaptable CSV workflow" sans jamais prétendre à une intégration API.

### Priorité 7 — Peer group percentiles
Les métriques d'un support ne sont plus jugées dans l'absolu : le détail du score affiche désormais sa position en percentile au sein de sa propre catégorie de méthodologie ("Top 18 %" sur le Sharpe, etc.), pour les critères où une comparaison a du sens (absent pour Private Equity / SCPI / structurés, qui n'ont pas de Sharpe classique — affiché explicitement plutôt que masqué).

### Priorité 10 — Simulation Monte Carlo (analyse interne)
Une vraie simulation (500 tirages gaussiens mensuels, pas une approximation décorative) calcule les 10ᵉ/25ᵉ/médiane/75ᵉ percentiles du capital projeté, ainsi qu'une probabilité indicative d'atteindre le montant cible de l'objectif prioritaire. Explicitement cantonnée à l'analyse interne (dossier interne uniquement, jamais le relevé client), avec un disclaimer sur ses limites méthodologiques.

### Priorité 12 — Internal Investment Memo restructuré (bug corrigé)
Le dossier interne affichait auparavant des blocs JSON bruts (`<pre>${JSON.stringify(...)}</pre>`) — une pratique explicitement interdite par le cahier des charges V12. Entièrement reconstruit en **17 sections structurées** (Client Overview, Objectives, Existing Portfolio, Diagnostic, Risk Analytics, Strategic Allocation, Investment Search Mandate, Candidate Universe, Products Rejected, Selected Products, Committee Views, Stress Tests, Suitability, Human Overrides, Audit Trail, Final Recommendation, Compliance Notice), entièrement en tableaux et texte lisibles.

### Priorité 13 — Investment Decision Log avec acteurs
Chaque entrée de l'audit trail identifie désormais explicitement son acteur (Système / Screening / Comité / Analyste), au lieu d'un flux de texte non attribué.

### Priorité 14 — Market Intelligence structurel/tactique plafonné
Les convictions du comité sont séparées en **Structural View** (long terme : actions US/Europe/émergents) et **Tactical View** (court/moyen terme : IG/HY/duration), avec un badge affichant explicitement le plafond de leur poids dans le score final (10 % par défaut, connecté à la vraie formule de blend de la Priorité 6 — donc réellement appliqué, pas seulement affirmé).

### Priorité 15 — Opportunity Watchlist
Watchlist fonctionnelle (thème, classe d'actif, thèse, catalyseurs, risques, horizon, statut), extensible par l'analyste, non intégrée automatiquement au scoring — sert la recherche future comme demandé.

### Priorités 17 / 19 / 21 — Statuts explicites, state management, marquage des données
- Chaque étape affiche désormais un statut parmi **Draft / System Proposal / Analyst Reviewed / Validated** (au lieu d'un badge binaire), avec une sémantique réfléchie : une saisie humaine directe (dossier client, import Quantalys) passe à *Validated* ; un calcul système (audit, scoring, contrôles) reste *System Proposal* tant qu'aucune décision humaine n'a été enregistrée ; une décision d'analyste sur un support fait passer l'étape à *Analyst Reviewed*.
- Les recherches Quantalys de démonstration et le bouton "Voir la démonstration" sont explicitement marqués **Demo Data** ; la volatilité estimée et les projections sont marquées **Estimated**.
- `resetAll()` remet effectivement tous les statuts à *Draft*, confirmant que le state management (Priorité 19) est cohérent de bout en bout.

### Ce qui reste consciemment non traité
- **Priorité 11** (relevé client pédagogique en 10 pages avec pagination dédiée) — non tenté : la refonte visuelle complète du rendu paginé aurait nécessité plus de temps qu'il n'en restait pour être fait sérieusement plutôt que superficiellement.
- **Priorité 16** (monitoring post-investissement : suivi de performance vs benchmark, percentile, style drift dans le temps) — délibérément écarté. Un prototype à session unique sans persistance ne peut pas montrer un historique de positions dans le temps sans fabriquer des données fictives non vérifiables ; plutôt que de simuler quelque chose de creux, ce module est documenté ici comme non traité.
- **Priorité 22** (polish narratif final du cas de démonstration) — déjà largement satisfait par le cas CLIENT-DEMO-001 construit au fil des itérations précédentes (portefeuille initial volontairement imparfait, objectifs multiples, résolution progressive visible à chaque étape) ; pas retouché spécifiquement dans cette session.

## V11 — Advisory Workflow (Phases 1 à 6)

Cette itération corrige le défaut principal identifié à l'audit de la V10 : les modules d'analyse avancés (stress tests, overlap, suitability, comité d'investissement, private markets, produits structurés) existaient côté moteur Python mais n'étaient pas connectés au parcours interactif. Le parcours (`docs/index.html`) suit désormais les 9 étapes réelles d'un dossier client, et toutes les méthodologies ci-dessous sont recalculées **en direct** sur le portefeuille effectivement construit par l'utilisateur (et non sur un portefeuille de démonstration figé) :


**1. Dossier client → 2. Audit → 3. Allocation → 4. Quantalys / CSV → 5. Sélection financière → 6. Portefeuille recommandé → 7. Contrôles & stress tests → 8. Préconisation → 9. Reporting.**

### Profil client (Phase 2)
- Profil de risque dérivé de 5 dimensions réelles — horizon, capacité financière de perte, risque maximal accepté, **réaction psychologique déclarée à une perte de 15 %**, expérience financière — avec l'explication complète affichée ("Pourquoi ce profil ?"), pas seulement une étiquette.
- Objectifs multiples avec montant cible, priorité et horizon propres.

### Audit patrimonial & portefeuille existant (Phase 3)
- Détection de redondances appliquée aussi au **portefeuille existant** du client (pas seulement au portefeuille cible).
- Alerte sur l'exposition change non couverte (devise de cotation ≠ exposition réelle au risque de change).

### Sélection financière différenciée (Phase 4)
- **7 méthodologies de scoring distinctes** : ETF, OPCVM actif, Obligataire, Alternatifs génériques, **Private Equity** (IRR/TVPI/DPI/maturité du vintage), **SCPI** (distribution/occupation) et **Produits structurés** (coupon/distance à la barrière) — chacune configurable dans Investment Policy. Les supports illiquides ne sont plus pénalisés par une grille générique inadaptée à leur nature.
- Éligibilité et **vue Comité d'investissement** (Approved/Watch/Review/Reject) calculées automatiquement mais toujours distinctes de la décision de l'analyste — tout écart est tracé dans l'audit trail (human-in-the-loop réel, pas seulement affiché).

### Portefeuille cible & contrôles (Phase 5)
- Construction du portefeuille cible uniquement à partir des supports Approved, comparaison avant/après.
- **Stress tests** : 5 scénarios (choc actions, taux, crédit, change, risk-off) appliqués au portefeuille cible réel.
- **Suitability matrix** : score pondéré allocation / risque / liquidité / coût / diversification, statut Compatible / À ajuster / Inadapté.
- **Private Markets & Produits structurés** : vues dédiées (IRR/TVPI/DPI, distribution SCPI, scénarios de barrière) dès qu'un support de ce type est retenu.

### Data Quality & robustesse (Phase 6)
- **Data Quality Monitor** sur chaque import Quantalys : score de complétude, ISIN manquants/dupliqués, métriques manquantes, formats invalides — affiché *avant* toute analyse.
- Robustesse testée sur des imports volontairement malformés : aucun `NaN`/`undefined`/traceback n'est jamais affiché à l'écran.
- **38 supports de démonstration** (ETF, OPCVM, obligataire, Private Equity, SCPI, produits structurés) avec des métriques fictives mais cohérentes par classe d'actif.

### Ajustements du 3ᵉ passage — recentrage sur le workflow réel du cabinet

- **Trois recherches Quantalys pré-chargées et cumulables** (Cœur de portefeuille / Diversification / Poche alternative), au lieu d'un unique export : reproduit la réalité d'un analyste qui exporte plusieurs recherches Quantalys puis les combine, plutôt qu'un import unique et figé.
- **Projection à horizon sur 3 scénarios (Prudent / Central / Optimiste)** appliquée au portefeuille cible réellement construit, avec confrontation explicite à chaque objectif chiffré du client (« objectif atteignable » / « objectif non couvert à ce stade ») — intégrée à la fois dans l'onglet Contrôles, le brouillon de préconisation et le relevé client. Hypothèses de rendement fictives et clairement indiquées comme telles.
- **Ajustement manuel des métriques d'un support** directement depuis le tableau de scoring (TER, Sharpe, drawdown, encours, score qualitatif, IRR, distribution, coupon selon le type de support), avec recalcul immédiat du score et traçabilité complète (ancienne valeur → nouvelle valeur, raison) dans l'audit trail — le human-in-the-loop porte désormais aussi sur les données, pas seulement sur la décision finale.
- **Décomposition du score affichée** (Intrinsèque / Client Fit / Conviction du comité), pour que l'analyste comprenne immédiatement pourquoi un support est bien ou mal noté, sans avoir à deviner.
- Correction d'un artefact d'affichage (concentration immobilière pouvant dépasser 100 % du patrimoine net en cas de fort effet de levier).

### Tests

```bash
python -m pytest              # moteur Python (scoring, stress tests, suitability, overlap, comité…)
npm install && npm test       # parcours interactif complet, simulé en DOM headless (jsdom)
```

La suite `npm test` déroule le parcours démo de bout en bout (dossier client → audit → allocation → import Quantalys → scoring → comité → portefeuille cible → contrôles → préconisation → reporting), vérifie l'absence d'erreurs JavaScript, et rejoue un import CSV volontairement malformé pour confirmer qu'aucune anomalie n'est masquée. À ce stade (fin de la session V12) : **64 assertions côté parcours interactif + 9 tests côté moteur Python**, tous verts, couvrant explicitement chacune des priorités listées ci-dessus (ex. non-régression du bug "Sharpe favorable" sur un fonds sans Sharpe, cohérence des statuts après reset, absence de JSON brut dans le dossier interne).

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
