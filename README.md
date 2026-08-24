# DATA CORE — Omega Logistics

Projet guidé de refonte de l'infrastructure data d'Omega Logistics.

## Étape 1

Objectif : préparer l'environnement, initialiser PostgreSQL, importer les 7 CSV FluxPro et réaliser les premiers contrôles SQL.

### Prérequis

- Git
- Docker Desktop / Docker Engine + Docker Compose
- Python 3.11+ recommandé

### 1. Initialiser Git

```bash
git init
git add .
git commit -m "chore: initialiser le projet DATA CORE"
```

### 2. Configurer l'environnement Python

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### 3. Démarrer PostgreSQL

```bash
docker compose up -d postgres
docker compose ps
```

L'image PostgreSQL 16 initialise automatiquement le schéma depuis `postgres/init/`.

### 4. Importer les 7 CSV

```bash
python scripts/load_fluxpro.py
```

### 5. Lancer les contrôles SQL

```bash
docker compose exec postgres psql -U omega -d omega -f /dev/stdin < sql/01_controles.sql
```

Ou entrer dans psql:

```bash
docker compose exec postgres psql -U omega -d omega
```

puis:

```sql
\dt
SELECT COUNT(*) FROM commandes;
```

### 6. API pédagogique fournie

Dans un second terminal:

```bash
cd dataset/api
python app.py
```

Puis:

```bash
curl http://127.0.0.1:5050/api/health
curl -H "X-API-Key: datacore-training-2026" http://127.0.0.1:5050/api/transporteurs
```

## Structure

- `dataset/` : pack fourni par le cahier des charges
- `scripts/` : scripts d'ingestion et d'exploitation
- `sql/` : requêtes SQL
- `postgres/` : initialisation PostgreSQL
- `docs/` : documentation du projet
- `bloc2/` : collecte, nettoyage, API
- `bloc3/` : OMEGA BI
- `bloc4/` : OMEGA LAKE

## Principe

Les données fournies restent inchangées dans `dataset/`. Les transformations métier seront réalisées dans les pipelines du projet afin de conserver une source de référence reproductible.
