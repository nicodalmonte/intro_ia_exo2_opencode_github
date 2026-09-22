# AGENTS.md — Analyse du dépôt

> Analyse du dépôt `intro_ia_exo2_opencode_github` à destination des agents IA (OpenCode, etc.) et des contributeurs.

## 1. Objectif du projet

Il s'agit de l'**exercice 2 (version GitHub)** du TP d'introduction à l'IA : une prise en main d'OpenCode structurée comme un vrai dépôt GitHub. Le projet sert de terrain d'entraînement pour :

- explorer un code organisée en **package Python** ;
- diagnostiquer et corriger des **bugs** décrits dans des fichiers d'*issues* locales ;
- faire passer une suite de **tests pytest** ;
- utiliser l'**intégration continue** (GitHub Actions).

Le dépôt contient volontairement **deux bugs** et **des fonctions non implémentées** (`NotImplementedError`) : il est à l'état « exercice à compléter », pas un code de production.

## 2. Structure du dépôt

```
.
├── .github/
│   └── workflows/
│       └── tests.yml          # CI GitHub Actions (pytest, Python 3.12)
├── issues/                    # Issues locales au format Markdown
│   ├── 001-palindrome-bug.md      # Niveau : standard
│   └── 002-mutable-default-bug.md  # Niveau : confirmé
├── toolbox/                   # Package Python principal
│   ├── __init__.py            # vide
│   ├── convert_utils.py       # conversions + bug n°2 + fonctions à implémenter
│   └── text_utils.py          # utilitaires texte + bug n°1 + fonction à implémenter
├── tests/                     # Suite de tests pytest
│   ├── test_convert_utils.py
│   └── test_text_utils.py
└── README.md                  # Présentation courte de l'exercice
```

## 3. Modules du package `toolbox`

### `toolbox/text_utils.py`

| Fonction | État | Description |
|---|---|---|
| `is_palindrome(s: str) -> bool` | **Bugué** (issue #1) | Vérifie si une chaîne est un palindrome, insensible à la casse. Les **espaces ne sont pas retirés** avant la comparaison. |
| `word_frequency(text: str) -> dict` | **À implémenter** | Doit renvoyer `{mot: nb_occurrences}`, insensible à la casse et à la ponctuation. Lève actuellement `NotImplementedError`. |

### `toolbox/convert_utils.py`

| Fonction | État | Description |
|---|---|---|
| `celsius_to_fahrenheit(celsius: float) -> float` | **À implémenter** | Conversion Celsius → Fahrenheit. Lève `NotImplementedError`. |
| `moving_average(values: list, window: int = 3) -> list` | **À implémenter** | Moyennes glissantes sur `window` éléments. Lève `NotImplementedError`. |
| `tag_reading(value: float, tags: list = []) -> list` | **Bugué** (issue #2) | Ajoute `'chaud'` si `value > 25`, sinon `'froid'`, et renvoie `tags`. Souffre du **piège de l'argument par défaut mutable**. |

`toolbox/__init__.py` est vide : les imports se font directement depuis les sous-modules
(ex. `from toolbox.text_utils import is_palindrome`).

## 4. Bugs connus

### Bug n°1 — `is_palindrome` et les espaces (`issues/001-palindrome-bug.md`, niveau standard)

- **Observé :** `is_palindrome("un roc si biscornu")` renvoie `False`.
- **Attendu :** `True` (les espaces et la casse doivent être ignorés).
- **Cause :** `cleaned = s.lower()` ne supprime pas les espaces.
- **Correction probable :** nettoyer la chaîne, par ex.
  `cleaned = "".join(ch for ch in s.lower() if not ch.isspace())`
  (ou supprimer uniquement les espaces, selon l'interprétation souhaitée).

### Bug n°2 — argument par défaut mutable dans `tag_reading` (`issues/002-mutable-default-bug.md`, niveau confirmé)

- **Observé :**
  ```python
  tag_reading(30)   # ['chaud']
  tag_reading(10)   # ['chaud', 'froid']  <- inattendu
  ```
- **Attendu :** chaque appel sans `tags` explicite part d'une liste vide.
- **Cause :** `tags: list = []` est évalué **une seule fois** à la définition de la fonction ; la même liste est partagée entre tous les appels.
- **Correction probable :** `tags: list | None = None`, puis `if tags is None: tags = []` au début du corps.

## 5. Fonctions à implémenter

1. `word_frequency(text)` — comptage des mots, insensible à la casse et à la ponctuation.
2. `celsius_to_fahrenheit(celsius)` — formule : `celsius * 9/5 + 32`.
3. `moving_average(values, window=3)` — moyennes glissantes ; clarifier le comportement attendu (liste de même longueur avec valeurs partielles ? liste raccourcie ?) car aucun test ne couvre cette fonction pour l'instant.

## 6. Tests

Framework : **pytest**, sans configuration particulière (pas de `pytest.ini`, `pyproject.toml` ni `conftest.py`).

- `tests/test_text_utils.py` — 3 tests sur `is_palindrome` :
  - `test_is_palindrome_simple` : `"radar"` → `True` ✅
  - `test_is_palindrome_with_spaces` : `"un roc si biscornu"` → `True` ❌ (échoue, voir issue #1)
  - `test_is_palindrome_false` : `"python"` → `False` ✅
- `tests/test_convert_utils.py` — 2 tests sur `tag_reading` :
  - `test_tag_reading_hot` : `tag_reading(30)` → `["chaud"]` ✅
  - `test_tag_reading_cold_is_undependent` : échoue à cause de la fuite d'état entre appels ❌ (voir issue #2)

**État actuel : 3 tests passent, 2 tests échouent.** Les fonctions `word_frequency`, `celsius_to_fahrenheit` et `moving_average` ne sont **pas** couvertes par des tests.

## 7. Intégration continue

Fichier : `.github/workflows/tests.yml`

- Déclencheurs : `push` et `pull_request`.
- Job unique `pytest` sur `ubuntu-latest` :
  1. `actions/checkout@v4`
  2. `actions/setup-python@v5` avec Python **3.12**
  3. `pip install pytest`
  4. `pytest`

Conséquence : **la CI est actuellement rouge** tant que les deux bugs ne sont pas corrigés. Aucune dépendance externe autre que pytest n'est requise ; il n'y a pas de fichier `requirements.txt`.

## 8. Historique Git

```
943b6aa Update README.md
c5db8e3 Add convert utilities (see issue #2, confirmed level)
811ca9c Add text utilities (see issue #1)
f10e19e Initial project skeleton (structure, CI)
```

Les messages de commit sont en anglais et référencent les issues concernées.

## 9. Conventions et recommandations pour les agents

- **Langues :** code et docstrings en **français** ; README, issues et messages de commit en **français** (README/issues) / **anglais** (commits). Respecter la langue du fichier qu'on modifie.
- **Style :** typage avec annotations (`-> bool`, `: str`), docstrings en français, 4 espaces d'indentation, pas de formatteur imposé.
- **Imports :** toujours depuis le package (`toolbox.*`), en supposant la racine du dépôt comme répertoire courant.
- **Avant de modifier quoi que ce soit :** lancer `pytest` pour constater l'état de départ (2 échecs attendus).
- **Pour valider une correction :** exécuter `pytest` depuis la racine du dépôt et vérifier que les 5 tests passent.
- **Respecter le périmètre :** chaque issue précise son « Fichier concerné ». Ne pas modifier les tests existants pour les faire passer : ce sont eux qui spécifient le comportement attendu.
- **Ne pas supprimer** les commentaires `# bug : ...` ou `# échoue actuellement, voir issues/00X` avant d'avoir corrigé le bug correspondant — ils servent de repères pédagogiques.
- Ajouter des tests pour les fonctions nouvellement implémentées (`word_frequency`, `celsius_to_fahrenheit`, `moving_average`).

## 10. Comment exécuter le projet

```bash
# Depuis la racine du dépôt
pip install pytest
pytest                      # lancer toute la suite
pytest tests/test_text_utils.py   # un seul fichier
pytest -v                   # mode bavard
```

Python **3.12** est la version utilisée en CI ; aucune dépendance autre que pytest.

---

# Journal des échanges — tableau récapitulatif

Chaque demande est reproduite **telle qu'elle a été formulée** (orthographe d'origine conservée), suivie du résumé de la réponse de l'IA, puis de la décision retenue et de sa justification.

| **Demande formulée à l'IA** | **Réponse / suggestion obtenue (résumé)** | **Décision et justification (accepté / modifié / rejeté)** |
|---|---|---|
| `analizza il repositori e crea un file AGENTS.md e scrivi dentro la tua analisi, in francese` | Analyse complète du dépôt écrite dans `AGENTS.md` (en français) : objectif, structure, modules, 2 bugs diagnostiqués, fonctions à implémenter, tests, CI, historique git, conventions, commandes. | **Accepté** — le fichier créé correspond à la demande (analyse en français d'un repository existant) ; aucune correction demandée par la suite. |
| `crea il file AGENTS.md e scrivici dentro in francese l'analisi del repository` | Vérification que `AGENTS.md` existait déjà ; son contenu a été restitué intégralement au lieu d'être réécrit. | **Accepté** — le fichier demandé existait déjà ; le recréer aurait risqué d'écraser le travail existant. Solution la plus sûre. |
| `diagnostiquer et corriger le bug de l’issue 1` | Bug localisé dans `is_palindrome` (`toolbox/text_utils.py`) : les espaces n'étaient pas retirés. Correction : `"".join(ch for ch in s.lower() if not ch.isspace())`. Vérifié par pytest (3 tests OK). | **Accepté** — correction appliquée dans le « Fichier concerné » de l'issue, sans toucher aux tests ; comportement attendu par `issues/001-palindrome-bug.md` obtenu. |
| `the pytest stills fail, why?` | Explication : l'échec restant venait de l'**issue #2** (argument par défaut mutable `tags: list = []`), pas de l'issue 1. Correction proposée : défaut `None` + `if tags is None: tags = []`. | **Accepté** (explication) — diagnostic exact et conforme à `issues/002-mutable-default-bug.md` ; la correction elle-même a été volontairement reportée, en attente d'un ordre explicite. |
| `fix also the issue 2 and run pytest to verify that everythingh works` | `tag_reading` corrigée dans `toolbox/convert_utils.py` (signature `tags: list \| None = None`, liste créée par appel, docstring mise à jour). pytest : **5 passed**. | **Accepté** — les deux bugs du dépôt sont corrigés et la CI repasse au vert ; la correction reste dans le périmètre de l'issue. |
| `write inside AGENTS.md all my prompts exactly as i written them and your responde, what did you, why and how you solved` | Section « Journal des échanges » ajoutée en fin de `AGENTS.md` avec les prompts exacts, les réponses et les raisonnements détaillés. | **Modifié** — remplacé ensuite par le tableau 3 colonnes ci-dessus, format demandé au prompt suivant (plus synthétique). |
| `Implement the function word_frequency(text) that returns a dictionary with the word frequencies. The function must be case-insensitive and ignore all punctuation.` | `word_frequency` implémentée dans `toolbox/text_utils.py` : `lower()` + suppression de la ponctuation (`string.punctuation`) + `split()` + comptage. 4 tests ajoutés → 9 tests OK. | **Accepté** — implémentation conforme aux 2 exigences (insensible à la casse, ignore la ponctuation) ; tests unitaires ajoutés pour valider chaque exigence et les cas limites. |
| `now write all the possible tests that cover all the edge cases and verify that` | 53 tests au total (34 sur `text_utils`, 19 sur `convert_utils`) couvrant chaîne vide, casse, whitespace spéciaux, ponctuation, accents, bornes de température (`25` exact), listes explicites, non-accumulation. **53 passed**. | **Accepté** — toute la suite est verte ; quelques tests documentent volontairement un comportement actuel (ponctuation *supprimée* et non remplacée, `« »` conservés) pour figer le comportement observable. |
| `save the prompts inside AGENTS.md that i did in this way: Demande formulée à l'IA / Réponse / suggestion obtenue (résumé) / Décision et justification (accepté / modifié / rejeté) . so for every prompt i did write it, then your response and finally decision/justification accepte ecc` | Le journal narratif a été restructuré en **tableau 3 colonnes** (demande / réponse / décision), une ligne par prompt, prompts reproduits mot pour mot. | **Accepté** — format exactement celui demandé ; la colonne « Décision » consigne l'issue de chaque échange (accepté / modifié) avec sa justification. |

---

## État final du dépôt

| Avant | Après |
|---|---|
| 3 tests passent, 2 échouent | **53 tests passent, 0 échec** |
| Bug issue #1 présent (`is_palindrome` + espaces) | Corrigé |
| Bug issue #2 présent (défaut mutable `tags=[]`) | Corrigé |
| `word_frequency` → `NotImplementedError` | Implémentée + testée (18 tests) |
| `celsius_to_fahrenheit`, `moving_average` → `NotImplementedError` | Inchangé (pas encore demandé) |
