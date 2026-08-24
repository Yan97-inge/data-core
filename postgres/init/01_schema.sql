-- DATA CORE / PostgreSQL
-- Schéma générique pour importer les CSV "FluxPro" dans le SGBD de votre choix
-- (PostgreSQL, MySQL, SQLite...). Syntaxe SQL standard ; adaptez les types si
-- besoin selon le moteur retenu (ex. AUTOINCREMENT / SERIAL / AUTO_INCREMENT).
-- Ordre de création important (clés étrangères).

CREATE TABLE entrepots (
  id                  INTEGER PRIMARY KEY,
  code                VARCHAR(20)  NOT NULL,
  nom                 VARCHAR(100) NOT NULL,
  ville               VARCHAR(100) NOT NULL,
  capacite_palettes   INTEGER
);

CREATE TABLE clients (
  id       INTEGER PRIMARY KEY,
  code     VARCHAR(30)  NOT NULL,
  nom      VARCHAR(100) NOT NULL,
  secteur  VARCHAR(100)
);

CREATE TABLE produits (
  id                    INTEGER PRIMARY KEY,
  sku                   VARCHAR(20) NOT NULL,
  libelle               VARCHAR(150) NOT NULL,
  client_id             INTEGER REFERENCES clients(id),
  categorie             VARCHAR(50),
  poids_kg              DECIMAL(6,2),
  temperature_dirigee   BOOLEAN
);

CREATE TABLE commandes (
  id             INTEGER PRIMARY KEY,
  client_id      INTEGER REFERENCES clients(id),
  entrepot_id    INTEGER REFERENCES entrepots(id),
  date_commande  DATE,
  statut         VARCHAR(30)
);

CREATE TABLE lignes_commande (
  id            INTEGER PRIMARY KEY,
  commande_id   INTEGER REFERENCES commandes(id),
  produit_id    INTEGER REFERENCES produits(id),
  quantite      INTEGER
);

CREATE TABLE expeditions (
  id                       INTEGER PRIMARY KEY,
  commande_id              INTEGER REFERENCES commandes(id),
  tracking_number          VARCHAR(20) NOT NULL,
  transporteur             VARCHAR(100),
  date_expedition          DATE,
  date_livraison_prevue    DATE,
  date_livraison_reelle    DATE,
  statut                   VARCHAR(30)
);

CREATE TABLE stocks (
  id            INTEGER PRIMARY KEY,
  entrepot_id   INTEGER REFERENCES entrepots(id),
  produit_id    INTEGER REFERENCES produits(id),
  quantite      INTEGER,
  date_maj      DATE
);

-- Import des CSV correspondants (exemple avec le client psql ; adaptez la
-- commande à votre SGBD : \copy pour psql, LOAD DATA pour MySQL,
-- .import pour sqlite3, ou l'assistant d'import de votre client graphique) :
--
-- \copy entrepots        FROM 'entrepots.csv'        DELIMITER ',' CSV HEADER;
-- \copy clients           FROM 'clients.csv'           DELIMITER ',' CSV HEADER;
-- \copy produits          FROM 'produits.csv'          DELIMITER ',' CSV HEADER;
-- \copy commandes         FROM 'commandes.csv'         DELIMITER ',' CSV HEADER;
-- \copy lignes_commande   FROM 'lignes_commande.csv'   DELIMITER ',' CSV HEADER;
-- \copy expeditions       FROM 'expeditions.csv'       DELIMITER ',' CSV HEADER;
-- \copy stocks            FROM 'stocks.csv'            DELIMITER ',' CSV HEADER;
