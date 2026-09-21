# DATA CORE — Omega Logistics

Projet de refonte de l'infrastructure data d'Omega Logistics.

Ce dépôt contient les travaux réalisés autour de la préparation de l'environnement, de l'initialisation PostgreSQL, de l'import des données FluxPro, du profilage des données et de la consolidation des fichiers de commandes clients.

---

## 1. État actuel du projet

Les travaux actuellement réalisés et validés portent sur :

* l'initialisation du projet Git ;
* la configuration de l'environnement Python ;
* la mise en place de PostgreSQL avec Docker Compose ;
* l'import des données CSV fournies ;
* les premiers contrôles qualité SQL ;
* le profilage des fichiers de commandes clients ;
* la normalisation de trois sources clients ;
* la consolidation des commandes clients dans un format commun ;
* l'intégration de la table consolidée dans PostgreSQL ;
* les contrôles de cohérence sur les produits, les entrepôts, les dates, les quantités et les clients ;
* la validation finale de la consolidation avec un statut de contrôle `OK`.

Les répertoires `bloc2/`, `bloc3/` et `bloc4/` sont présents dans l'arborescence du projet mais ne sont pas encore documentés comme réalisés dans cette version.

---

## 2. Prérequis

Les outils utilisés sont :

* Git ;
* Docker Desktop / Docker Engine avec Docker Compose ;
* Python 3.11 ou version ultérieure recommandée ;
* PostgreSQL 16 via Docker.

---

## 3. Structure du projet

```text
data-core/
│
├── dataset/
│   ├── api/
│   │   ├── fixtures/
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   ├── data/
│   │   ├── clients.csv
│   │   ├── clients_fichiers/
│   │   │   ├── freshmarket_commandes.csv
│   │   │   ├── mediotex_commandes.csv
│   │   │   └── norddrive_commandes.csv
│   │   ├── commandes.csv
│   │   ├── entrepots.csv
│   │   ├── expeditions.csv
│   │   ├── historique/
│   │   ├── iot/
│   │   ├── lignes_commande.csv
│   │   ├── produits.csv
│   │   ├── schema.sql
│   │   └── stocks.csv
│   │
│   └── output/
│       └── clients_consolides.csv
│
├── docs/
│   └── 01_inspection_donnees.md
│
├── postgres/
│   └── init/
│       └── 01_schema.sql
│
├── scripts/
│   ├── check_client_duplicates.py
│   ├── inspect_normalization_duplicates.py
│   ├── load_fluxpro.py
│   ├── normalize_clients.py
│   ├── profile_clients.py
│   └── start_api.sh
│
├── sql/
│   ├── 01_controles.sql
│   ├── 02_clients_consolides.sql
│   └── 03_controles_clients_consolides.sql
│
├── bloc2/
├── bloc3/
├── bloc4/
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

## 4. Configuration de l'environnement

Le fichier `.env` est utilisé pour la configuration locale et n'est pas versionné.

Un fichier `.env.example` est fourni comme modèle :

```env
POSTGRES_DB=omega
POSTGRES_USER=omega
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
API_PORT=5050
```

Sous Windows PowerShell :

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Le fichier `.env` reste local.

Le `.gitignore` exclut notamment :

```text
.venv/
.env
.env.*
postgres/data/
*.dump
*.sql.gz
```

---

## 5. Démarrage de PostgreSQL

PostgreSQL est exécuté avec Docker Compose.

Démarrer le service :

```powershell
docker compose up -d postgres
```

Vérifier son état :

```powershell
docker compose ps
```

Le schéma PostgreSQL est initialisé à partir du contenu de :

```text
postgres/init/01_schema.sql
```

---

## 6. Import des données FluxPro

Le script d'import est :

```text
scripts/load_fluxpro.py
```

Lancer l'import :

```powershell
python scripts/load_fluxpro.py
```

Les données sources sont conservées dans `dataset/data/`.

Le principe retenu est de conserver les données fournies comme source de référence et de réaliser les transformations dans les scripts et pipelines du projet.

---

## 7. Contrôles initiaux

Les premiers contrôles SQL sont regroupés dans :

```text
sql/01_controles.sql
```

Ils peuvent être exécutés avec :

```powershell
Get-Content .\sql\01_controles.sql | docker compose exec -T postgres psql -U omega -d omega
```

---

# 8. Profilage et consolidation des fichiers clients

Trois sources de commandes clients ont été traitées :

| Source      | Fichier                     |
| ----------- | --------------------------- |
| NordDrive   | `norddrive_commandes.csv`   |
| FreshMarket | `freshmarket_commandes.csv` |
| MedioTex    | `mediotex_commandes.csv`    |

Chaque source possède son propre format de colonnes.

Le script :

```text
scripts/normalize_clients.py
```

normalise les différentes structures vers un schéma commun.

---

## 9. Schéma consolidé

Le fichier produit est :

```text
dataset/output/clients_consolides.csv
```

Il contient 9 colonnes :

```text
source
reference_commande
date_commande
reference_produit
designation_produit
quantite
entrepot_destination
poids_unitaire_g
chaine_froid_requise
```

Les dates sont normalisées au format :

```text
YYYY-MM-DD
```

Les valeurs numériques sont converties en valeurs numériques lorsque cela est possible.

Les doublons exacts présents après normalisation sont supprimés.

---

## 10. Résultat de la consolidation

La dernière exécution validée produit :

```text
Nombre total de lignes : 4178
Nombre de colonnes : 9
```

Répartition par source :

| Source      | Nombre de lignes |
| ----------- | ---------------: |
| FreshMarket |             1283 |
| MedioTex    |             1456 |
| NordDrive   |             1439 |
| **Total**   |         **4178** |

---

## 11. Données manquantes

Les contrôles montrent :

```text
Quantités manquantes : 56
Dates manquantes : 0
```

Répartition des quantités manquantes :

| Source      | Lignes | Quantités manquantes | Pourcentage |
| ----------- | -----: | -------------------: | ----------: |
| FreshMarket |   1283 |                   27 |      2,10 % |
| MedioTex    |   1456 |                    0 |      0,00 % |
| NordDrive   |   1439 |                   29 |      2,02 % |

Les quantités renseignées ne contiennent aucune valeur nulle ou négative.

Les 56 quantités manquantes sont donc conservées comme valeurs manquantes et ne sont pas remplacées arbitrairement.

---

## 12. Contrôles de normalisation

Un contrôle spécifique des doublons créés par la normalisation a été réalisé avec :

```text
scripts/inspect_normalization_duplicates.py
```

Ce contrôle a identifié 8 doublons créés par la normalisation, soit 16 lignes concernées avant suppression.

Ces doublons ont ensuite été supprimés lors de la consolidation.

Le fichier final présente :

```text
Doublons exacts après consolidation : 0
```

---

# 13. Intégration dans PostgreSQL

La table cible est :

```text
clients_consolides
```

Elle est créée par :

```text
sql/02_clients_consolides.sql
```

Le fichier consolidé est ensuite importé dans PostgreSQL avec `COPY`.

Exemple :

```powershell
Get-Content .\dataset\output\clients_consolides.csv |
docker compose exec -T postgres psql -U omega -d omega -c "\copy clients_consolides(source,reference_commande,date_commande,reference_produit,designation_produit,quantite,entrepot_destination,poids_unitaire_g,chaine_froid_requise) FROM STDIN WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')"
```

Résultat validé :

```text
COPY 4178
```

---

## 14. Contrôles PostgreSQL

La structure de la table `clients_consolides` contient notamment :

```text
source
reference_commande
date_commande
reference_produit
designation_produit
quantite
entrepot_destination
poids_unitaire_g
chaine_froid_requise
```

Les contrôles complémentaires sont regroupés dans :

```text
sql/03_controles_clients_consolides.sql
```

Exécution :

```powershell
Get-Content .\sql\03_controles_clients_consolides.sql |
docker compose exec -T postgres psql -U omega -d omega
```

---

# 15. Résultats des contrôles qualité

Les contrôles actuellement validés donnent les résultats suivants :

| Contrôle                   | Résultat |
| -------------------------- | -------: |
| Total des lignes           |     4178 |
| Dates manquantes           |        0 |
| Doublons exacts            |        0 |
| Produits inconnus          |        0 |
| Entrepôts inconnus         |        0 |
| Libellés incohérents       |        0 |
| Quantités non positives    |        0 |
| Incohérences source/client |        0 |
| Statut global              |   **OK** |

La période des commandes présentes dans la table consolidée est :

```text
Date minimale : 2025-01-01
Date maximale : 2026-07-31
```

---

## 16. Correspondance avec le référentiel produits

Les références produits consolidées correspondent au champ `sku` du référentiel `produits`.

Le contrôle suivant ne détecte aucun produit inconnu :

```sql
SELECT COUNT(*) AS produits_inconnus
FROM clients_consolides cc
LEFT JOIN produits p
    ON p.sku = cc.reference_produit
WHERE p.id IS NULL;
```

Résultat :

```text
0
```

Une vérification des libellés entre les commandes consolidées et le référentiel produits ne détecte également aucune incohérence.

---

## 17. Correspondance avec les entrepôts

Les destinations utilisées dans les fichiers clients sont :

```text
OMG-LIL
OMG-LYO
OMG-MAR
```

Elles correspondent au référentiel des entrepôts.

Répartition actuelle :

| Entrepôt | Ville     | Nombre de lignes |
| -------- | --------- | ---------------: |
| OMG-LIL  | Lille     |             1374 |
| OMG-LYO  | Lyon      |             1392 |
| OMG-MAR  | Marseille |             1412 |

Aucun entrepôt inconnu n'a été détecté.

---

## 18. Répartition des produits par source

Les trois sources utilisent chacune 10 références produits distinctes.

| Source      | Commandes distinctes | Produits distincts | Entrepôts distincts |
| ----------- | -------------------: | -----------------: | ------------------: |
| FreshMarket |                  441 |                 10 |                   3 |
| MedioTex    |                  493 |                 10 |                   3 |
| NordDrive   |                  466 |                 10 |                   3 |

---

## 19. Scripts disponibles

### Profilage

```text
scripts/profile_clients.py
```

Permet d'effectuer le profilage des fichiers clients.

### Contrôle des doublons

```text
scripts/check_client_duplicates.py
```

Permet de rechercher les doublons dans les données clients.

### Normalisation

```text
scripts/normalize_clients.py
```

Normalise les trois sources clients et produit :

```text
dataset/output/clients_consolides.csv
```

### Inspection des doublons après normalisation

```text
scripts/inspect_normalization_duplicates.py
```

Permet d'identifier les doublons apparus après la transformation vers le schéma commun.

### Import FluxPro

```text
scripts/load_fluxpro.py
```

Permet l'import des données fournies dans PostgreSQL.

---

## 20. Scripts SQL

| Fichier                                   | Rôle                                  |
| ----------------------------------------- | ------------------------------------- |
| `sql/01_controles.sql`                    | Contrôles initiaux des données        |
| `sql/02_clients_consolides.sql`           | Création de la table consolidée       |
| `sql/03_controles_clients_consolides.sql` | Contrôles qualité de la consolidation |

---

## 21. API pédagogique

Le dépôt contient également une API pédagogique fournie dans :

```text
dataset/api/
```

Elle comprend notamment :

```text
dataset/api/app.py
dataset/api/fixtures/
dataset/api/requirements.txt
```

L'API peut être lancée avec :

```powershell
cd dataset/api
python app.py
```

Les endpoints présents dans le projet peuvent être testés localement avec les commandes documentées dans le code et les fixtures fournies.

Cette API fait partie du contenu fourni avec le projet ; son évolution métier n'est pas documentée comme un développement réalisé dans cette étape.

---

## 22. Données sources

Les données fournies sont conservées dans :

```text
dataset/data/
```

Elles comprennent notamment :

* clients ;
* commandes ;
* lignes de commandes ;
* produits ;
* entrepôts ;
* stocks ;
* expéditions ;
* historique des expéditions ;
* données IoT ;
* fichiers de commandes des différents clients.

Les données sources ne sont pas modifiées directement par le processus de normalisation.

Les transformations sont réalisées par les scripts du projet afin de conserver une source de référence reproductible.

---

## 23. Éléments non encore réalisés

Les répertoires suivants existent dans l'arborescence mais ne sont pas considérés comme réalisés dans l'état actuel du projet :

```text
bloc2/
bloc3/
bloc4/
tests/
```

Ce README ne présente donc pas ces parties comme terminées.

---

## 24. Reproductibilité

Pour reproduire la partie actuellement validée du projet :

### 1. Préparer l'environnement

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### 2. Démarrer PostgreSQL

```powershell
docker compose up -d postgres
```

### 3. Importer les données

```powershell
python scripts/load_fluxpro.py
```

### 4. Normaliser les fichiers clients

```powershell
python scripts/normalize_clients.py
```

### 5. Créer la table consolidée

```powershell
Get-Content .\sql\02_clients_consolides.sql |
docker compose exec -T postgres psql -U omega -d omega
```

### 6. Importer le fichier consolidé

```powershell
Get-Content .\dataset\output\clients_consolides.csv |
docker compose exec -T postgres psql -U omega -d omega -c "\copy clients_consolides(source,reference_commande,date_commande,reference_produit,designation_produit,quantite,entrepot_destination,poids_unitaire_g,chaine_froid_requise) FROM STDIN WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')"
```

### 7. Exécuter les contrôles

```powershell
Get-Content .\sql\03_controles_clients_consolides.sql |
docker compose exec -T postgres psql -U omega -d omega
```

Le résultat attendu pour le contrôle global est :

```text
statut_controle
-----------------
OK
```

---

## 25. Git

Le projet est versionné avec Git sur la branche :

```text
main
```

Les fichiers de configuration locale et données PostgreSQL persistées ne sont pas destinés à être versionnés.

Avant tout commit, vérifier :

```powershell
git status
```

Puis :

```powershell
git diff
```

Les fichiers sensibles, notamment `.env`, doivent rester ignorés par Git.

---

## 26. État de validation

À ce stade, la partie profilage, normalisation et consolidation des données clients est validée.

Résultat final :

```text
4178 lignes
9 colonnes
0 doublon exact
0 date manquante
56 quantités manquantes
0 produit inconnu
0 entrepôt inconnu
0 libellé incohérent
0 quantité non positive
0 incohérence source/client
Statut : OK
```

La suite du projet pourra s'appuyer sur cette base consolidée et contrôlée.
