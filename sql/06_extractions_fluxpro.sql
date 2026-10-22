-- C9 - Requêtes SQL d'extraction FluxPro
-- DATA CORE / Omega Logistics

-- 1. Commandes avec client et entrepôt
SELECT
    c.id AS commande_id,
    c.date_commande,
    c.statut,
    cl.nom AS client,
    e.code AS entrepot
FROM commandes c
JOIN clients cl
    ON cl.id = c.client_id
JOIN entrepots e
    ON e.id = c.entrepot_id
ORDER BY c.date_commande, c.id;


-- 2. Détail des lignes de commande
SELECT
    lc.commande_id,
    lc.produit_id,
    p.sku,
    p.libelle,
    lc.quantite
FROM lignes_commande lc
JOIN produits p
    ON p.id = lc.produit_id
ORDER BY lc.commande_id, lc.produit_id;


-- 3. Stocks par entrepôt et produit
SELECT
    s.entrepot_id,
    e.code AS entrepot,
    s.produit_id,
    p.sku,
    p.libelle,
    s.quantite
FROM stocks s
JOIN entrepots e
    ON e.id = s.entrepot_id
JOIN produits p
    ON p.id = s.produit_id
ORDER BY e.code, p.sku;


-- 4. Expéditions avec commande, client et entrepôt
SELECT
    ex.id AS expedition_id,
    ex.commande_id,
    ex.date_expedition,
    ex.statut,
    cl.nom AS client,
    e.code AS entrepot
FROM expeditions ex
JOIN commandes c
    ON c.id = ex.commande_id
JOIN clients cl
    ON cl.id = c.client_id
JOIN entrepots e
    ON e.id = c.entrepot_id
ORDER BY ex.date_expedition, ex.id;


-- 5. Historique volumineux des expéditions
SELECT
    id,
    client,
    entrepot,
    categorie_produit,
    date_expedition,
    poids_kg,
    delai_livraison_jours,
    cout_transport_eur,
    statut
FROM historique_expeditions
ORDER BY date_expedition, id;


-- 6. Synthèse historique par client et entrepôt
SELECT
    client,
    entrepot,
    COUNT(*) AS nombre_expeditions,
    SUM(poids_kg) AS poids_total_kg,
    AVG(delai_livraison_jours) AS delai_moyen_jours,
    SUM(cout_transport_eur) AS cout_transport_total_eur
FROM historique_expeditions
GROUP BY client, entrepot
ORDER BY client, entrepot;