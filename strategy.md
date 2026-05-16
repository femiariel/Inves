# Stratégie d'investissement — Alloc PEA

## Vue d'ensemble

Deux moteurs distincts, deux comptes, une seule discipline : pas de décision discrétionnaire.

| Sleeve | Compte | Allocation | Moteur |
|--------|--------|-----------|--------|
| Core PEA | PEA (Euronext .PA) | 80% DCAM.PA fixe | Ancre long terme |
| Satellite PEA | PEA (Euronext .PA) | 20% maxi | Momentum composite |
| **Sleeve A** | **Saxo (UCITS)** | **Poche spéculative** | **Momentum cross-sectionnel + filtre MM200** |

---

## Sleeve A — Momentum Cross-Sectionnel avec Filtre de Tendance

### Objectif

Capter l'essentiel des hausses de marché tout en limitant le drawdown maximum à ~20% sur la poche allouée. Stratégie systématique mensuelle, zéro discrétion.

### Univers (22 ETFs actifs + 1 défensif)

#### Sectoriels US S&P 500 (11)
| Ticker | Nom |
|--------|-----|
| IUIT | iShares S&P 500 IT Sector |
| IUFS | iShares S&P 500 Financials |
| IUES | iShares S&P 500 Energy |
| IUHC | iShares S&P 500 Health Care |
| IUCD | iShares S&P 500 Consumer Discretionary |
| IUIS | iShares S&P 500 Industrials |
| IUCS | iShares S&P 500 Consumer Staples |
| IUUS | iShares S&P 500 Utilities |
| IUMS | iShares S&P 500 Materials |
| IURE | iShares S&P 500 Real Estate |
| IUCM | iShares S&P 500 Communication Services |

#### Géographiques (5)
| Ticker | Nom |
|--------|-----|
| IWDA | iShares Core MSCI World |
| EIMI | iShares Core MSCI EM IMI |
| SJPA | iShares Core MSCI Japan IMI |
| CEU | iShares Core MSCI Europe |
| NDIA | iShares MSCI India |

#### Factor / Style (3)
| Ticker | Nom |
|--------|-----|
| IUSM | iShares S&P SmallCap 600 |
| IS3R | iShares MSCI World Momentum Factor |
| IWQU | iShares MSCI World Quality Factor |

#### Thématiques (2)
| Ticker | Nom |
|--------|-----|
| SEMI | VanEck Semiconductor UCITS ETF |
| WBIO | Rize Medical Innovation UCITS ETF |

#### Or (1)
| Ticker | Nom |
|--------|-----|
| SGLD | Invesco Physical Gold ETC |

#### Défensif
| Ticker | Nom | Rôle |
|--------|-----|------|
| XEON | Xtrackers EUR Overnight Rate Swap | Refuge obligatoire en régime OFF |

---

### Signaux

#### 1. Filtre de régime absolu — IWDA vs SMA(200)

```
Si prix_IWDA(J) ≥ moyenne(prix_IWDA sur 200 derniers jours) → Régime ON
Si prix_IWDA(J) <  moyenne(prix_IWDA sur 200 derniers jours) → Régime OFF
```

**Pourquoi IWDA comme filtre :**
IWDA (MSCI World) représente le marché actions mondial développé — c'est le beta pur. Utiliser le même instrument sur compte Saxo évite un biais de change ou de liquidité qu'introduirait SPY (USD). La SMA200 est empiriquement la frontière la plus robuste entre régime haussier et baissier sur données historiques longues (Faber 2007, Antonacci 2014). Sa lenteur est une feature, pas un bug : elle élimine les faux signaux sur volatilité intra-mois.

**Pourquoi un filtre absolu plutôt que cross-sectionnel :**
Le momentum cross-sectionnel dit "qui monte le plus" mais ne dit pas "est-ce qu'il faut être investi du tout". Sans filtre absolu, Sleeve A reste investi en plein bear market en achetant les secteurs qui tombent le moins vite. Le filtre MM200 impose une sortie propre : si tout le marché est en tendance baissière, on n'est pas en marché, point.

#### 2. Momentum cross-sectionnel — 6 mois

```
Score(i) = Prix(i, J) / Prix(i, J−126) − 1
```

126 jours ouvrés ≈ 6 mois calendaires.

**Pourquoi 6 mois :**
La littérature académique sur le momentum (Jegadeesh & Titman 1993, Asness et al. 2013) identifie la fenêtre 6–12 mois comme celle où l'effet est le plus persistant et statistiquement significatif. La fenêtre 1 mois est dominée par le mean-reversion à court terme. La fenêtre 12 mois capte davantage de retournements sectoriels. 6 mois est le sweet spot : signal suffisamment fort pour être actionnable, suffisamment lent pour ne pas churner.

**Pourquoi total return brut (pas de z-score) :**
Sleeve A ne cherche pas à comparer des pommes et des oranges entre secteurs de volatilité très différente. Le classement brut par rendement favorise naturellement les actifs qui ont eu à la fois de la direction et de la force. C'est intentionnellement différent du momentum composite (stratégie PEA) qui normalise par MAD pour égaliser les volatilités — ici on veut précisément les ETFs qui ont le plus monté, sans égalisation.

---

### Règle de sélection avec garde-fou corrélation

#### Régime ON

```
1. Calculer Score(i) pour chacun des 22 ETFs actifs
2. Trier par Score décroissant
3. Parcourir le classement de manière greedy :
   - Si aucun ETF sélectionné encore : prendre le #1
   - Pour chaque candidat suivant :
       Si |corr(candidat, ETF déjà sélectionné)| > 0.80 sur 126 jours → ignorer
       Sinon → ajouter à la sélection
   - S'arrêter quand 2 ETFs sélectionnés
4. Allouer 50% / 50% sur les 2 ETFs retenus
   (ou 100% si un seul passe le garde-fou)
```

**Pourquoi le garde-fou corrélation :**
Sans contrôle, le top-2 peut être deux secteurs US technologiquement proches (ex. IUIT + SEMI) avec corrélation > 0.95. Dans ce cas, la diversification est cosmétique — on a deux fois le même pari. Le garde-fou à 0.80 garantit qu'il y a un minimum de diversification réelle. Le seuil 0.80 est délibérément permissif : il bloque les quasi-doublons (IUIT/SEMI) sans exclure des paires légitimement corrélées comme deux secteurs US cycliques.

**Pourquoi greedy plutôt qu'optimisation :**
Une optimisation MV ou CVaR nécessite des estimations de covariance stables — ce qui est difficile sur un univers de 22 ETFs avec peu d'historique commun. Le greedy déterministe sur ranking + corrélation est transparent, reproductible, et ne souffre pas d'overfitting. La règle de discipline l'exige : le signal commande, pas une boîte noire.

**Pourquoi 50/50 et pas pondération par momentum :**
La pondération égale est l'allocation la plus robuste quand on choisit délibérément 2 actifs comme "meilleurs" — ils ont déjà été sélectionnés parce qu'ils sont bons, surpondérer le #1 vs le #2 revient à ajouter une décision supplémentaire non justifiée. L'égal-pondération est aussi la plus transparente pour l'exécution.

#### Régime OFF

```
100% XEON — EUR Overnight Rate Swap (monétaire EUR, risque quasi-nul)
```

**Pourquoi XEON et pas cash :**
XEON réplique l'€STR (taux de dépôt BCE). En régime de taux positifs, ça rapporte entre 2 et 4% annualisé sans risque de duration. C'est supérieur au cash sur compte courant et sans risque de crédit. C'est aussi un ETF coté : l'exécution est identique à un achat d'ETF actions, aucune friction administrative.

---

### Calendrier d'exécution (non négociable)

| Étape | Quand |
|-------|-------|
| Évaluation des signaux | Dernier jour ouvré du mois, à la clôture |
| Exécution des ordres | Premier jour ouvré du mois suivant, à l'ouverture |
| Durée de la procédure | 15–20 minutes |

**Pourquoi mensuel :**
Un rebalancement trop fréquent (hebdomadaire) augmente les coûts de transaction et le bruit du signal. Un rebalancement trop rare (trimestriel) rate les rotations sectorielles rapides. Mensuel est le standard de la littérature momentum : assez fréquent pour capturer les rotations, assez rare pour que les coûts restent négligeables.

---

### Règles de discipline (non négociables)

1. **Pas de discrétion.** Aucune décision basée sur news, macro, intuition ou conviction personnelle. Le signal commande, point.

2. **Pas d'override.** Si le signal dit IUCM à 50%, c'est IUCM à 50% même si tu penses que les medias sont surévalués.

3. **Pas de skip de rebalancement.** Même en période de volatilité élevée. Le filtre MM200 gère la protection — il n'appartient pas à l'investisseur de doubler le filtre par inaction.

4. **Pas de modification de paramètres.** Lookback 6M, MM200, Top-2, seuil 0.80 — tous fixés définitivement. Toute modification après avoir observé les résultats est du data-snooping.

5. **Pas d'exception sur le filtre.** Si IWDA < SMA200 en fin de mois → 100% XEON le lendemain, sans discussion.

---

### Différences avec la stratégie satellite PEA

| Dimension | Satellite PEA | Sleeve A |
|-----------|--------------|---------|
| Signal | Momentum composite (12M, 6M, 3M, SMA200, vol, DD) | Momentum 6M brut uniquement |
| Normalisation | Z-score MAD cross-sectionnel | Retour total brut |
| Filtre régime | Aucun (SMA200 dans le score, pas en binaire) | Binaire ON/OFF sur IWDA SMA200 |
| Positions | Top-5 avec déduplication corrélation | Top-2 avec déduplication corrélation |
| Refuge | Cash partiel selon stress | 100% XEON |
| Univers | ~400 ETFs Euronext Paris (.PA), PEA-éligibles | 22 ETFs UCITS Saxo |
| Pondération | Proportionnelle au score | Égal (50/50) |
| Rebalancement | Drift > 1% déclenche ordre | Mensuel systématique |

**Pourquoi deux stratégies différentes :**
La stratégie PEA est contrainte par l'enveloppe fiscale (uniquement ETFs .PA) et est construite pour optimiser dans cet univers limité. Sleeve A est une stratégie momentum "pure" sur un univers plus large et plus homogène (sectoriels S&P 500), sans contrainte PEA, donc plus proche de la littérature académique canonique.

---

## Stratégie Satellite PEA (80/20)

### Structure

| Sleeve | Poids | Contenu |
|--------|-------|---------|
| Core | 80% | DCAM.PA (Amundi PEA MSCI World) — ancre fixe |
| Satellite | 0–20% | Top-5 ETFs .PA momentum composite |
| Cash | Reste | Buffer si stress élevé ou pas d'ETF éligibles |

### Formule de score (0–100)

```
score = 35 + 12 × factor_score    (clippé à [0, 100])
```

Où `factor_score` :
```
+ 0.45 × z(momentum 12-1M)   ← signal principal
+ 0.18 × z(momentum 6M)
+ 0.10 × z(momentum 3M)
+ 0.17 × z(prix / SMA200)    ← confirmation de tendance
− 0.06 × z(vol annualisée)   ← pénalité volatilité
− 0.04 × z(max drawdown 12M) ← pénalité drawdown
− overheat_penalty            ← si z(1M) > 1.5 : pénaliser les spikes
```

**Baseline 35** : un ETF z-score = 0 sur tous les facteurs obtient 35. Score ≥ 65 = achat, 50–65 = hold, 35–50 = alléger, < 35 = éviter.

**Z-scoring MAD** : robuste aux outliers (1.4826 × MAD), winsorisé 1–99%, cappé ±3σ. Cross-sectionnel : comparaison dans l'univers valide à chaque date.

### Filtres d'éligibilité satellite

Un ETF doit passer TOUS ces filtres :
1. ≥ 253 jours de données valides
2. Prix au-dessus de SMA(200)
3. Momentum 12-1M > 0
4. Qualité de données : pas de mouvement journalier > 100%, rendement lookback ≤ 300%, vol annuelle ≤ 300%
5. Filtre produit : exclusion des ETFs leveragés, inverses, short, matières premières (pétrole, or, argent, blé, cuivre...), carbone

### Sizing stress-aware

Index de stress composite (0–100) à partir de 5 indicateurs :
- VIX term structure (VIX9D/VIX3M) : poids 30%
- SKEW index : poids 15%
- Semivariance RS⁻/RS⁺ : poids 20%
- HYG vs SMA200 (proxy spread HY) : poids 20%
- XLF vs SPY 20j (santé secteur financier) : poids 15%

Budget satellite :
- Stress < 60 (calme) : budget = 20%
- Stress 60–75 (vigilance) : budget ∝ linéaire 20% → 10%
- Stress > 75 (élevé) : budget → 0%, tout en cash

**Pourquoi le stress-aware :**
Le momentum pur investit même quand le marché est en régime de panique asymétrique (spreads HY en écartement, VIX en backwardation). Le stress composite ajoute un garde-fou systémique sans modifier les scores — il réduit le budget satellite plutôt que d'exclure des ETFs individuels.

### Rebalancement

Seuil de drift : différence absolue de poids > 1% déclenche un ordre achat/vente. En dessous = hold.