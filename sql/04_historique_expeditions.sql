CREATE TABLE IF NOT EXISTS historique_expeditions (
    id BIGINT PRIMARY KEY,
    client VARCHAR(30) NOT NULL,
    entrepot VARCHAR(30) NOT NULL,
    categorie_produit VARCHAR(50) NOT NULL,
    date_expedition DATE NOT NULL,
    poids_kg NUMERIC(10,2) NOT NULL CHECK (poids_kg > 0),
    delai_livraison_jours INTEGER NOT NULL CHECK (delai_livraison_jours >= 0),
    cout_transport_eur NUMERIC(12,2) NOT NULL CHECK (cout_transport_eur > 0),
    statut VARCHAR(20) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_historique_expeditions_date
    ON historique_expeditions (date_expedition);

CREATE INDEX IF NOT EXISTS idx_historique_expeditions_client
    ON historique_expeditions (client);

CREATE INDEX IF NOT EXISTS idx_historique_expeditions_entrepot
    ON historique_expeditions (entrepot);