-- ============================================================
-- CONTRÔLES QUALITÉ : clients_consolides
-- ============================================================

-- 1. Volume total
SELECT
    COUNT(*) AS total_lignes
FROM clients_consolides;


-- 2. Répartition par source
SELECT
    source,
    COUNT(*) AS nb_lignes
FROM clients_consolides
GROUP BY source
ORDER BY source;


-- 3. Quantités manquantes par source
SELECT
    source,
    COUNT(*) AS nb_lignes,
    COUNT(*) FILTER (WHERE quantite IS NULL) AS quantites_manquantes,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE quantite IS NULL)
        / COUNT(*),
        2
    ) AS pct_quantites_manquantes
FROM clients_consolides
GROUP BY source
ORDER BY source;


-- 4. Quantités invalides
SELECT
    COUNT(*) AS quantites_non_positives
FROM clients_consolides
WHERE quantite IS NOT NULL
  AND quantite <= 0;


-- 5. Produits inconnus
SELECT
    COUNT(*) AS produits_inconnus
FROM clients_consolides cc
LEFT JOIN produits p
    ON p.sku = cc.reference_produit
WHERE p.id IS NULL;


-- 6. Entrepôts inconnus
SELECT
    COUNT(*) AS entrepots_inconnus
FROM clients_consolides cc
LEFT JOIN entrepots e
    ON e.code = cc.entrepot_destination
WHERE e.id IS NULL;


-- 7. Cohérence des libellés produits
SELECT
    COUNT(*) AS libelles_incoherents
FROM clients_consolides cc
JOIN produits p
    ON p.sku = cc.reference_produit
WHERE LOWER(TRIM(cc.designation_produit))
      <> LOWER(TRIM(p.libelle));


-- 8. Doublons exacts
SELECT
    COUNT(*) AS doublons_exacts
FROM (
    SELECT
        source,
        reference_commande,
        date_commande,
        reference_produit,
        designation_produit,
        quantite,
        entrepot_destination,
        poids_unitaire_g,
        chaine_froid_requise,
        COUNT(*) AS nb
    FROM clients_consolides
    GROUP BY
        source,
        reference_commande,
        date_commande,
        reference_produit,
        designation_produit,
        quantite,
        entrepot_destination,
        poids_unitaire_g,
        chaine_froid_requise
    HAVING COUNT(*) > 1
) d;


-- 9. Dates
SELECT
    MIN(date_commande) AS date_min,
    MAX(date_commande) AS date_max,
    COUNT(*) FILTER (WHERE date_commande IS NULL) AS dates_manquantes
FROM clients_consolides;


-- 10. Répartition par entrepôt
SELECT
    cc.entrepot_destination,
    e.nom,
    e.ville,
    COUNT(*) AS nb_lignes
FROM clients_consolides cc
JOIN entrepots e
    ON e.code = cc.entrepot_destination
GROUP BY
    cc.entrepot_destination,
    e.nom,
    e.ville
ORDER BY cc.entrepot_destination;


-- 11. Cohérence source / client du produit
SELECT
    COUNT(*) AS incoherences_source_client
FROM clients_consolides cc
JOIN produits p
    ON p.sku = cc.reference_produit
JOIN clients c
    ON c.id = p.client_id
WHERE UPPER(cc.source) <> UPPER(c.nom);


-- 12. Contrôle final global
SELECT
    CASE
        WHEN COUNT(*) = 4178
         AND COUNT(*) FILTER (WHERE date_commande IS NULL) = 0
         AND COUNT(*) FILTER (
                WHERE quantite IS NOT NULL
                  AND quantite <= 0
             ) = 0
         AND COUNT(*) FILTER (
                WHERE quantite IS NULL
             ) = 56
        THEN 'OK'
        ELSE 'A VERIFIER'
    END AS statut_controle
FROM clients_consolides;