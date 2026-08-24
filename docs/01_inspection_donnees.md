# Étape 1 — Inspection initiale des données

## Sources FluxPro

| Fichier | Lignes | Colonnes | Doublons | NULL |
|---|---:|---:|---:|---:|
| entrepots.csv | 3 | 5 | 0 | 0 |
| clients.csv | 3 | 4 | 0 | 0 |
| produits.csv | 30 | 7 | 0 | 0 |
| commandes.csv | 1 400 | 5 | 0 | 0 |
| lignes_commande.csv | 4 186 | 4 | 0 | 0 |
| expeditions.csv | 1 100 | 8 | 0 | 339 |
| stocks.csv | 90 | 5 | 0 | 0 |

### Observation

Les 339 NULL de `expeditions` sont principalement à traiter comme une donnée métier à qualifier, et non comme une erreur à supprimer automatiquement : une livraison non encore réalisée peut légitimement ne pas avoir de date réelle.

## Fichiers clients hétérogènes

Les trois sources utilisent des structures différentes :

- NordDrive : `;` comme séparateur, formats de date multiples et champ `poids_unitaire_g`.
- FreshMarket : séparateur `,`, noms de colonnes spécifiques et indicateur de chaîne du froid.
- MedioTex : séparateur `,`, noms de colonnes spécifiques.

Le pipeline du bloc 2 devra standardiser ces trois structures vers un modèle commun.

## Données massives / IoT

Le pack contient :

- `omega_historique_expeditions.csv` : historique volumineux ;
- `capteurs_temperature.csv` ;
- `geoloc_flotte.csv` ;
- `camera_comptage.csv` ;
- `rfid_scans.json`.

## API

L'API Flask fournie est utilisée dans les blocs 2 et 4, conformément au cahier des charges.
