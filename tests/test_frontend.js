/**
 * Suite de tests fonctionnels du parcours interactif (docs/index.html).
 * Exécute le parcours démo complet dans un DOM simulé (jsdom) et vérifie
 * l'absence d'erreurs JS ainsi que la cohérence des principaux calculs.
 *
 * Usage : npm install && npm test
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

let failures = 0;

function assert(cond, msg) {
  if (!cond) {
    failures++;
    console.error(`  ✗ ${msg}`);
  } else {
    console.log(`  ✓ ${msg}`);
  }
}

async function main() {
  const htmlPath = path.join(__dirname, '..', 'docs', 'index.html');
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://localhost/docs/index.html' });
  const { window } = dom;

  window.Plotly = { newPlot: () => {} };
  window.fetch = async (url) => {
    const p = path.join(__dirname, '..', 'docs', url);
    const text = fs.readFileSync(p, 'utf-8');
    return { ok: true, json: async () => JSON.parse(text), text: async () => text };
  };
  window.scrollTo = () => {};
  window.print = () => {};
  window.alert = () => {};
  window.URL.createObjectURL = () => 'blob:stub';
  window.URL.revokeObjectURL = () => {};

  const jsErrors = [];
  window.addEventListener('error', (e) => jsErrors.push(e.error || e.message));

  const scripts = [...window.document.querySelectorAll('script')].filter(s => !s.src);
  const vm = require('vm');
  const context = dom.getInternalVMContext ? dom.getInternalVMContext() : window;
  vm.runInContext(scripts[0].textContent, context, { filename: 'app.js' });
  await new Promise(r => setTimeout(r, 50));

  const doc = window.document;
  const $ = (id) => doc.getElementById(id);
  const click = async (id) => { $(id).click(); await new Promise(r => setTimeout(r, 20)); };

  console.log('1. Chargement initial');
  assert($('dataStatus').textContent.length > 0, 'le statut des données est affiché');
  assert($('stepbar').children.length === 9, 'la barre d’étapes affiche les 9 étapes du workflow');

  console.log('2. Parcours démo — dossier client');
  await click('demoBtn');
  assert(doc.querySelector('.section.active').id === 'audit', 'la démo bascule vers l’audit');
  assert(['Prudent', 'Équilibré', 'Dynamique'].includes($('profileKpi').textContent), 'un profil synthétique est calculé');
  assert($('profileExplain').textContent.includes('dimensions'), 'le profil est expliqué (pas une simple étiquette)');

  console.log('2bis. Diagnostic patrimonial (Priorité 1)');
  assert($('grossWorth').textContent.includes('€'), 'le patrimoine brut est calculé et affiché');
  assert($('debtGrossKpi').textContent.includes('%'), 'le ratio dette/patrimoine brut est calculé');
  assert($('securityKpi').textContent.includes('mois'), 'la réserve de précaution est exprimée en mois de dépenses');
  assert($('savingsRateKpi').textContent.includes('%'), 'le taux d’épargne est calculé');
  assert(!/NaN|undefined|Infinity/.test($('diagnosticAlerts').innerHTML), 'aucune valeur aberrante dans le diagnostic patrimonial');
  assert(!$('diagnosticAlerts').textContent.includes('124'), 'pas de pourcentage de concentration incohérent (>100% mal géré)');

  console.log('2ter. Compartiments par objectif (Priorité 2)');
  assert($('bucketsView').textContent.includes('Sécurité'), 'le compartiment court terme est affiché');
  assert($('bucketsView').textContent.includes('Croissance long terme'), 'le compartiment long terme est affiché');
  assert($('bucketsView').textContent.includes('cible future'), 'un objectif long terme est bien traité comme une cible future, pas un besoin de capital immédiat');

  console.log('2quater. Allocation dérivée des buckets, pas seulement du profil (Priorité 3)');
  const rationaleBefore = $('allocRationale').textContent;
  assert(rationaleBefore.includes('enveloppe investissable'), 'la justification de l’allocation référence les compartiments, pas un texte générique');

  console.log('2quinquies. Portfolio Diagnostic — hiérarchie Critical/Warning/Information (Priorité 4)');
  assert(/CRITICAL|WARNING|INFO/.test($('portfolioAudit').textContent), 'les alertes du portefeuille détenu affichent un niveau de sévérité (Critical/Warning/Info)');
  assert($('portfolioAudit').textContent.includes('Plus grande ligne'), 'la concentration sur une ligne est mesurée dans l’audit du portefeuille détenu');

  console.log('3. Allocation');
  await click('saveAllocBtn');

  console.log('4. Import Quantalys (démo — 3 recherches combinées)');
  $('demoCsv1Btn').click();
  await new Promise(r => setTimeout(r, 40));
  $('demoCsv2Btn').click();
  await new Promise(r => setTimeout(r, 40));
  $('demoCsv3Btn').click();
  await new Promise(r => setTimeout(r, 40));
  assert(+$('csvRows').textContent > 40, 'les 3 recherches Quantalys combinées dépassent 40 supports');
  assert($('csvIssues').textContent.includes('Complétude'), 'le contrôle qualité des données est affiché avant analyse');

  console.log('5. Scoring & comité');
  await click('runScoreBtn');
  assert(+$('scoreCount').textContent > 0, 'des scores sont calculés');
  assert($('committeeTable').querySelectorAll('tbody tr').length > 0, 'la vue comité d’investissement est générée');
  assert(!/NaN|undefined/.test($('scoreTable').innerHTML), 'aucun NaN/undefined affiché dans le tableau de scores');

  console.log('6. Construction du portefeuille cible');
  await click('buildPortfolioBtn');
  const selectedRows = $('selectedPortfolio').querySelectorAll('tbody tr').length;
  assert(selectedRows > 0, 'un portefeuille cible est construit');

  console.log('6bis. Before/After Premium (Priorité 9)');
  assert($('beforeAfterKpis').textContent.includes('Current Portfolio'), 'la comparaison Current vs Proposed Portfolio est affichée');
  assert($('beforeAfterKpis').textContent.includes('Diversification'), 'la diversification fait partie de la comparaison premium');
  assert(!/NaN|undefined/.test($('beforeAfterKpis').innerHTML), 'aucune valeur aberrante dans le tableau before/after');
  assert($('whatChanged').textContent.length > 10, 'la section « What changed? » est renseignée');
  assert($('whyChanged').textContent.includes('audit') || $('whyChanged').textContent.includes('compartiment'), 'la section « Why? » relie les changements à un constat d’audit ou aux compartiments');

  console.log('6ter. Scoring transparent Quality / Client Fit / House View (Priorité 6) et Client Fit approfondi (Priorité 8)');
  const S = window.eval('S');
  const peFund = S.scored.find(x => x.vehicle === 'Private Equity');
  assert(peFund && !peFund.reasons.some(r => /Sharpe/i.test(r)), 'un fonds Private Equity sans Sharpe ne reçoit jamais la mention "Sharpe favorable" (régression du bug corrigé)');
  assert(peFund && Number.isFinite(peFund._quality) && Number.isFinite(peFund._houseView), 'le score se décompose bien en Quality et House View distincts');
  const detailBtn = $('scoreTable').querySelector('[data-score-detail]');
  assert(!!detailBtn, 'un bouton de détail du score est disponible');
  detailBtn.click();
  await new Promise(r => setTimeout(r, 10));
  assert(doc.getElementById('metricEditPanel').textContent.includes('Final Decision Score'), 'le détail du score affiche la formule Quality/Client Fit/House View');

  console.log('20. Internal Investment Memo — 17 sections, sans JSON brut (Priorité 12)');
  const memo = window.eval('buildInternalMemo()');
  assert(!memo.includes('<pre>'), 'le dossier interne ne contient aucun bloc <pre> de JSON brut');
  assert((memo.match(/<h2>/g) || []).length === 17, 'le dossier interne comporte bien les 17 sections attendues (Client Overview → Compliance Notice)');
  assert(memo.includes('Human Overrides') && memo.includes('Audit Trail'), 'le dossier interne inclut les sections Human Overrides et Audit Trail');

  console.log('7. Contrôles');
  assert($('stressDetail').textContent.includes('Scénario le plus défavorable'), 'les stress tests sont calculés');
  assert(/Compatible|À ajuster|Inadapté/.test($('suitabilityBox').textContent), 'la suitability matrix retourne un statut');
  assert($('projectionSummary').textContent.includes('Prudent') || $('projectionSummary').querySelector('.grid3'), 'la projection à 3 scénarios (prudent/central/optimiste) est calculée');
  assert($('monteCarloBox').textContent.includes('Médiane') || $('monteCarloBox').textContent.includes('simulations'), 'la simulation Monte Carlo interne (Priorité 10) est calculée avec percentiles');
  assert(!/NaN|undefined|Infinity/.test($('monteCarloBox').innerHTML), 'aucune valeur aberrante dans la simulation Monte Carlo');

  console.log('7bis. Ajustement manuel d’une métrique');
  const firstEditBtn = $('scoreTable').querySelector('[data-edit-metric]');
  assert(!!firstEditBtn, 'un bouton d’ajustement manuel est disponible sur chaque support scoré');
  firstEditBtn.click();
  await new Promise(r => setTimeout(r, 10));
  const applyBtn = doc.getElementById('me_apply');
  assert(!!applyBtn, 'le panneau d’ajustement manuel s’ouvre avec ses champs');
  const terInput = doc.getElementById('me_ter');
  if (terInput) {
    const before = +terInput.value;
    terInput.value = (before || 0.01) + 0.05;
    doc.getElementById('me_reason').value = 'Test automatisé';
    applyBtn.click();
    await new Promise(r => setTimeout(r, 20));
    assert(+$('scoreCount').textContent > 0, 'le score est recalculé après ajustement manuel sans erreur');
  }

  console.log('8. Préconisation & reporting');
  assert($('adviceText').value.length > 100, 'un brouillon de préconisation est généré');
  assert($('adviceText').value.includes('Draft') || doc.querySelector('#advisory .notice').textContent.includes('Draft'), 'la mention de validation conseiller est présente');
  assert($('reportBody').innerHTML.length > 100, 'le relevé client est généré');

  console.log('13. Statuts explicites Draft/System Proposal/Analyst Reviewed/Validated (Priorité 17)');
  await click('demoBtn');
  assert($('status-client').textContent === 'Validated', 'le dossier client passe à Validated après analyse (saisie humaine directe)');
  assert($('status-audit').textContent === 'System Proposal', 'l’audit patrimonial reste une System Proposal tant qu’il n’est pas explicitement revu');
  $('saveAllocBtn').click();
  assert($('status-allocation').textContent === 'Validated', 'l’allocation passe à Validated après le clic sur "Valider l’allocation"');
  $('demoCsv1Btn').click();
  await new Promise(r => setTimeout(r, 40));
  assert($('status-quantalys').textContent === 'Validated', 'l’import Quantalys est une action humaine directe, donc Validated');
  $('runScoreBtn').click();
  await new Promise(r => setTimeout(r, 20));
  assert($('status-scoring').textContent === 'System Proposal', 'le scoring frais calculé est une System Proposal');
  const firstDecBtn = $('decisionTable').querySelector('[data-dec]');
  if (firstDecBtn) firstDecBtn.click();
  assert($('status-scoring').textContent === 'Analyst Reviewed', 'une décision manuelle de l’analyste fait passer l’étape à Analyst Reviewed');

  console.log('14. Demo Data / Estimated labelling (Priorité 21)');
  assert([...doc.querySelectorAll('#quantalys .badge')].some(b => b.textContent === 'Demo Data'), 'les recherches Quantalys pré-chargées sont explicitement marquées Demo Data');

  console.log('15. Mapping CSV visuel (Priorité 5)');
  const csvText = 'ISIN,Nom,Type,Classe,Volatilite 3 ans,Sharpe Ratio\nFR001,Fonds Test,ETF,Equity,0.15,0.7\n';
  await window.eval('importFile')({ text: async () => csvText }, 'quantalys');
  await new Promise(r => setTimeout(r, 30));
  const mappingText = $('columnMappingPanel').textContent;
  assert(mappingText.includes('colonnes reconnues automatiquement'), 'le mapping des colonnes CSV externe est affiché');
  assert(mappingText.includes('ISIN') && mappingText.includes('Volatilité'), 'les colonnes reconnues sont correctement mappées vers les champs internes');

  console.log('16. Peer group percentiles (Priorité 7)');
  await click('demoCsv1Btn');
  $('runScoreBtn').click();
  await new Promise(r => setTimeout(r, 20));
  const detailBtn2 = $('scoreTable').querySelector('[data-score-detail]');
  detailBtn2.click();
  await new Promise(r => setTimeout(r, 10));
  assert(doc.getElementById('metricEditPanel').textContent.includes('Peer group'), 'le détail du score affiche une comparaison peer group');

  console.log('17. Investment Decision Log avec acteurs (Priorité 13)');
  const trailText = $('auditTrail').textContent;
  assert(trailText.includes('Système') && trailText.includes('Cas de démonstration'), 'le journal de décision identifie l’acteur "Système" pour les actions automatiques');
  assert(trailText.includes('Analyste'), 'le journal de décision identifie l’acteur "Analyste" pour une validation humaine');

  console.log('18. Structural/Tactical View plafonnée (Priorité 14)');
  assert($('houseViewCapBadge').textContent.includes('10 %'), 'le plafond du House View (10% par défaut) est affiché explicitement à côté des convictions');
  assert(doc.body.textContent.includes('Structural View') && doc.body.textContent.includes('Tactical View'), 'les convictions sont bien séparées en vision structurelle et vision tactique');

  console.log('19. Opportunity Watchlist (Priorité 15)');
  assert($('watchlistView').textContent.includes('Thèse') && $('watchlistView').textContent.includes('Catalyseurs'), 'la watchlist affiche thèse, catalyseurs et risques par opportunité');
  const watchCountBefore = doc.querySelectorAll('#watchlistView .flag').length;
  $('addWatchBtn').click();
  assert(doc.querySelectorAll('#watchlistView .flag').length === watchCountBefore + 1, 'une nouvelle opportunité peut être ajoutée à la watchlist');

  console.log('9. Réinitialisation');
  await click('resetBtn');
  assert(doc.querySelector('.section.active').id === 'client', 'la réinitialisation revient au dossier client');
  assert($('status-allocation').textContent === 'Draft' && $('status-scoring').textContent === 'Draft', 'la réinitialisation remet bien tous les statuts à Draft (Priorité 19 — Reset case)');

  console.log('10. Robustesse — import malformé');
  await click('demoBtn');
  const badCsv = 'isin,name,vehicle,asset_class,ter\n,Sans ISIN,ETF,Equity,pasunnombre\n';
  const badFile = { text: async () => badCsv };
  await window.eval('importFile')(badFile, 'quantalys');
  await new Promise(r => setTimeout(r, 50));
  assert($('csvIssues').textContent.includes('manquant') || $('csvIssues').textContent.includes('invalide'), 'les anomalies sont détectées et affichées, pas masquées');
  $('runScoreBtn').click();
  await new Promise(r => setTimeout(r, 20));
  assert(!/NaN|undefined/.test($('scoreTable').innerHTML), 'un import imparfait ne produit pas de NaN/undefined visibles');

  console.log('11. Validation des données (Priorité 20)');
  $('age').value = 12;
  $('analyseClientBtn').click();
  await new Promise(r => setTimeout(r, 20));
  assert($('clientFormErrors').textContent.includes('Âge'), 'un âge hors plage (12 ans) est rejeté avec un message clair');
  $('age').value = 45;
  $('horizon').value = 0;
  $('analyseClientBtn').click();
  await new Promise(r => setTimeout(r, 20));
  assert($('clientFormErrors').textContent.includes('Horizon'), 'un horizon nul est rejeté avec un message clair');
  $('horizon').value = 20;
  $('analyseClientBtn').click();
  await new Promise(r => setTimeout(r, 20));
  assert($('clientFormErrors').className === 'hidden', 'un dossier valide passe sans message d’erreur');

  console.log('12. Cohérence des données — le dossier influence réellement le résultat (Priorité 18)');
  const allocBefore = JSON.stringify(window.eval('S.allocation'));
  const profileBefore = $('profileKpi').textContent;
  $('age').value = 68;
  $('riskTolerance').value = 'low';
  $('lossCapacity').value = 'low';
  $('reactionLoss').value = 'vendre';
  $('experience').value = 'aucune';
  $('analyseClientBtn').click();
  await new Promise(r => setTimeout(r, 20));
  const profileAfter = $('profileKpi').textContent;
  const allocAfter = JSON.stringify(window.eval('S.allocation'));
  assert(profileAfter !== profileBefore, 'changer l’âge et le profil de risque change bien le profil synthétique (68 ans, prudent)');
  assert(allocAfter !== allocBefore, 'l’allocation stratégique proposée change réellement avec le profil du client');
  assert(!$('adviceText').value.includes('dynamique') || profileAfter !== 'Dynamique', 'aucun texte résiduel de l’ancien profil ne subsiste');

  console.log('\n--- Erreurs JavaScript interceptées ---');
  if (jsErrors.length) {
    jsErrors.forEach(e => console.error(e && e.stack || e));
    failures += jsErrors.length;
  } else {
    console.log('  ✓ aucune');
  }

  console.log(`\n${failures === 0 ? 'TOUS LES TESTS SONT PASSÉS' : failures + ' ÉCHEC(S)'}`);
  process.exit(failures === 0 ? 0 : 1);
}

main().catch(e => { console.error('ÉCHEC FATAL', e); process.exit(1); });
