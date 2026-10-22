# 04 — Registre des traitements de données à caractère personnel



**Projet :** DATA CORE / OMEGA DATA

**Statut :** document de travail — validation organisationnelle et juridique requise

**Version :** 1.0



## 1. Objet et périmètre



Ce document recense les traitements de données repérables dans le dépôt DATA CORE à partir des fichiers de données, scripts, API et requêtes SQL.



Il constitue un inventaire technique préparatoire. Il ne remplace pas le registre officiel des activités de traitement du responsable de traitement. Les informations non démontrées par le dépôt sont marquées **À confirmer**.



## 2. Traitements recensés



### T01 — Importation et exploitation des données opérationnelles FluxPro



\- **Finalité technique :** charger et exploiter les données de clients, commandes, lignes de commande, produits, entrepôts, expéditions et stocks.

\- **Sources identifiées :** `dataset/data/clients.csv`, `commandes.csv`, `lignes_commande.csv`, `produits.csv`, `entrepots.csv`, `expeditions.csv`, `stocks.csv`.

\- **Opérations techniques :** import en base PostgreSQL, jointures, contrôles de qualité et requêtes d’extraction.

\- **Catégories de données :** identifiants et informations de clients, données de commandes et d’expéditions, données de stock et de produits.

\- **Personnes concernées :** À confirmer selon la nature des clients et des données importées.

\- **Base légale :** À confirmer.

\- **Destinataires et habilitations :** À confirmer.

\- **Durée de conservation :** À confirmer.

\- **Mesures de sécurité :** contrôles de qualité SQL et contraintes de base de données identifiés ; gestion des accès et chiffrement à vérifier.



### T02 — Consolidation et normalisation des fichiers clients



\- **Finalité technique :** harmoniser les formats de plusieurs fichiers clients et produire un fichier consolidé.

\- **Sources identifiées :** `dataset/data/clients_fichiers/freshmarket_commandes.csv`, `mediotex_commandes.csv`, `norddrive_commandes.csv`.

\- **Script identifié :** `scripts/normalize_clients.py`.

\- **Opérations techniques :** normalisation des colonnes, dates et quantités, consolidation et contrôles des doublons.

\- **Catégories de données :** références de commandes, dates, références et désignations de produits, quantités, entrepôts de destination et attributs logistiques.

\- **Personnes concernées :** À confirmer. Les références commerciales ne sont pas nécessairement des données personnelles, mais leur association à une personne physique peut le devenir.

\- **Base légale, destinataires et conservation :** À confirmer.

\- **Mesures identifiées :** scripts de profilage et de contrôle des doublons ; droits d’accès aux fichiers à vérifier.



### T03 — Historique des expéditions



\- **Finalité technique :** stocker et analyser l’historique des expéditions et produire des agrégations par client et entrepôt.

\- **Source identifiée :** `dataset/data/historique/omega_historique_expeditions.csv`.

\- **Script SQL identifié :** `sql/04_historique_expeditions.sql`.

\- **Catégories de données :** client, entrepôt, catégorie de produit, date d’expédition, poids, délai de livraison, coût de transport et statut.

\- **Personnes concernées :** À confirmer selon la nature des données clients et leur possibilité d’identification.

\- **Base légale, destinataires et conservation :** À confirmer.

\- **Mesures identifiées :** contraintes de validation et index en base ; contrôle des habilitations à vérifier.



### T04 — Collecte depuis l’API de transport



\- **Finalité technique :** récupérer les données de transporteurs, tournées et livraisons depuis l’API de démonstration.

\- **Sources identifiées :** `dataset/api/app.py` et les fichiers JSON de démonstration.

\- **Script identifié :** `scripts/collect_transflow_api.py`.

\- **Volume des fixtures inspectées :** 3 transporteurs, 139 tournées et 1 100 livraisons.

\- **Catégories de données :** identifiants de tournées et de livraisons, numéros de suivi, dates, statuts, horaires estimés et réels, identifiants de véhicules, noms de chauffeurs et contacts de transporteurs.

\- **Données potentiellement personnelles :** noms de chauffeurs, coordonnées de contact et adresses de livraison, selon les valeurs réellement présentes.

\- **Base légale, personnes concernées, destinataires et conservation :** À confirmer.

\- **Mesures identifiées :** contrôle par clé API dans l’application ; stockage des secrets, renouvellement des clés, journalisation et gestion des habilitations à vérifier.



### T05 — Collecte du portail transporteur



\- **Finalité technique :** extraire les informations de suivi exposées par le portail de démonstration.

\- **Script identifié :** `scripts/scrape_transport_portal.py`.

\- **Catégories de données :** numéro de suivi, statut, adresse de livraison et référence de tournée, selon les champs du portail.

\- **Personnes concernées :** À confirmer selon les données réelles ou fictives.

\- **Base légale et autorisation de collecte :** À confirmer.

\- **Destinataires et conservation :** À confirmer.

\- **Mesures identifiées :** script de collecte automatisée ; règles d’accès au portail et sécurisation des résultats à vérifier.



### T06 — Données IoT et suivi logistique



\- **Finalité technique :** ingérer et exploiter les données de comptage, de température, de géolocalisation de flotte et de scans RFID.

\- **Sources identifiées :**

&#x20; - `dataset/data/iot/camera_comptage.csv`

&#x20; - `dataset/data/iot/capteurs_temperature.csv`

&#x20; - `dataset/data/iot/geoloc_flotte.csv`

&#x20; - `dataset/data/iot/rfid_scans.json`

\- **Script identifié :** `scripts/load_rfid.py` pour l’import RFID ; schéma et requêtes d’import IoT dans `sql/05_iot.sql`.

\- **Catégories de données :** horodatages, entrepôts, zones, comptages, températures, identifiants de véhicules, coordonnées géographiques, vitesses, identifiants de palettes et références produit.

\- **Personnes potentiellement concernées :** chauffeurs ou personnels dont l’activité pourrait être associée à un véhicule, une localisation ou un horodatage ; présence effective de telles associations à confirmer.

\- **Base légale, destinataires et conservation :** À confirmer.

\- **Mesures identifiées :** contraintes de validation et index en base ; contrôle des accès aux données de localisation à vérifier.



### T07 — Exposition des données via l’API DATA CORE



\- **Finalité technique :** exposer des données logistiques via des routes HTTP et un flux de données de capteurs.

\- **Source identifiée :** `dataset/api/app.py`.

\- **Catégories de données :** informations de transporteurs, tournées, livraisons, statuts, horaires et données de capteurs.

\- **Personnes concernées :** À confirmer selon les données effectivement exposées.

\- **Authentification :** l’application vérifie une clé API sur les routes protégées ; l’efficacité de la configuration en production n’est pas établie.

\- **Destinataires et habilitations :** À confirmer.

\- **Journalisation, limitation d’accès, chiffrement en transit et gestion des incidents :** À vérifier.

\- **Base légale et conservation :** À confirmer.



## 3. Synthèse des catégories de données



| Catégorie | Exemples identifiés | Point de vigilance |

|---|---|---|

| Identification et contact | Nom de chauffeur, contact de transporteur | Vérifier s’il s’agit de personnes physiques identifiables |

| Localisation et livraison | Adresse de livraison, coordonnées de flotte | Vérifier la présence de données réelles et les accès autorisés |

| Activité logistique | Tournées, suivi, statuts et horaires | Une association à un chauffeur ou à un client peut permettre une identification |

| Données commerciales | Commandes, références clients, quantités et coûts | Vérifier si les clients sont des entreprises ou des personnes physiques |

| Données IoT | Température, comptage, RFID et horodatages | Vérifier si elles permettent indirectement d’identifier des personnes |



## 4. Mesures techniques à vérifier



Les éléments suivants doivent être examinés avant de considérer les mesures de sécurité comme validées :



\- \[ ] Vérifier que les fichiers et fixtures contiennent exclusivement des données fictives, ou identifier les données réelles.

\- \[ ] Confirmer les droits d’accès aux fichiers CSV/JSON et à la base PostgreSQL.

\- \[ ] Vérifier que les secrets ne sont pas codés en dur ni versionnés.

\- \[ ] Définir le stockage, la rotation et la révocation des clés API.

\- \[ ] Vérifier le chiffrement des communications et, si nécessaire, des données stockées.

\- \[ ] Définir la journalisation des accès et la durée de conservation des journaux.

\- \[ ] Documenter la sauvegarde, la restauration et la suppression des données.

\- \[ ] Vérifier les accès au portail de transport et les autorisations de collecte.

\- \[ ] Limiter l’accès aux données de localisation et aux coordonnées de livraison selon les besoins.

\- \[ ] Définir une procédure de gestion des incidents de sécurité.



## 5. Informations organisationnelles et juridiques à compléter



Les points suivants ne peuvent pas être déduits avec certitude du seul dépôt :



\- Identité et coordonnées du responsable de traitement.

\- Coordonnées du délégué à la protection des données, s’il y en a un.

\- Finalité métier précise et base légale de chaque traitement.

\- Catégories exactes de personnes concernées.

\- Destinataires, sous-traitants et responsabilités contractuelles.

\- Durées de conservation et règles de suppression.

\- Transferts éventuels hors de l’Espace économique européen.

\- Modalités d’information des personnes et d’exercice de leurs droits.

\- Nécessité d’une analyse d’impact relative à la protection des données.

\- Confirmation du caractère fictif, anonymisé ou réel de chaque jeu de données.



## 6. Conclusion



Le dépôt permet d’identifier plusieurs flux de traitement logistique, notamment la consolidation de fichiers clients, l’exploitation des données d’expédition, la collecte transporteur, le scraping du portail et l’ingestion de données IoT.



La présence de champs d’adresse, de contact, de chauffeur et de géolocalisation justifie une vérification de leur contenu réel et des possibilités d’identification. Ce document reste un inventaire technique préparatoire tant que les éléments organisationnels, juridiques et les mesures de sécurité non démontrées n’ont pas été validés.
