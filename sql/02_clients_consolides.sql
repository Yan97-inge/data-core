DROP TABLE IF EXISTS clients_consolides;

CREATE TABLE clients_consolides (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(30) NOT NULL,
    reference_commande VARCHAR(50) NOT NULL,
    date_commande DATE NOT NULL,
    reference_produit VARCHAR(50) NOT NULL,
    designation_produit VARCHAR(150) NOT NULL,
    quantite NUMERIC,
    entrepot_destination VARCHAR(30) NOT NULL,
    poids_unitaire_g NUMERIC,
    chaine_froid_requise VARCHAR(10)
);