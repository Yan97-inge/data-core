-- Premiers contrôles SQL DATA CORE

-- 1. Volumétrie
SELECT 'entrepots' AS table_name, COUNT(*) AS nb_lignes FROM entrepots
UNION ALL SELECT 'clients', COUNT(*) FROM clients
UNION ALL SELECT 'produits', COUNT(*) FROM produits
UNION ALL SELECT 'commandes', COUNT(*) FROM commandes
UNION ALL SELECT 'lignes_commande', COUNT(*) FROM lignes_commande
UNION ALL SELECT 'expeditions', COUNT(*) FROM expeditions
UNION ALL SELECT 'stocks', COUNT(*) FROM stocks
ORDER BY table_name;

-- 2. Doublons sur les clés primaires
SELECT id, COUNT(*) FROM entrepots GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM clients GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM produits GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM commandes GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM lignes_commande GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM expeditions GROUP BY id HAVING COUNT(*) > 1;
SELECT id, COUNT(*) FROM stocks GROUP BY id HAVING COUNT(*) > 1;

-- 3. Valeurs NULL attendues / à surveiller
SELECT
    COUNT(*) FILTER (WHERE date_livraison_reelle IS NULL) AS livraisons_reelles_manquantes,
    COUNT(*) FILTER (WHERE transporteur IS NULL) AS transporteurs_manquants,
    COUNT(*) AS total_expeditions
FROM expeditions;

-- 4. Intégrité référentielle
SELECT COUNT(*) AS commandes_client_inconnus
FROM commandes c
LEFT JOIN clients cl ON cl.id = c.client_id
WHERE cl.id IS NULL;

SELECT COUNT(*) AS commandes_entrepot_inconnus
FROM commandes c
LEFT JOIN entrepots e ON e.id = c.entrepot_id
WHERE e.id IS NULL;

SELECT COUNT(*) AS lignes_commande_inconnues
FROM lignes_commande lc
LEFT JOIN commandes c ON c.id = lc.commande_id
WHERE c.id IS NULL;

SELECT COUNT(*) AS lignes_produit_inconnus
FROM lignes_commande lc
LEFT JOIN produits p ON p.id = lc.produit_id
WHERE p.id IS NULL;

-- 5. Dates incohérentes
SELECT COUNT(*) AS expedition_avant_commande
FROM expeditions e
JOIN commandes c ON c.id = e.commande_id
WHERE e.date_expedition < c.date_commande;

SELECT COUNT(*) AS livraison_avant_expedition
FROM expeditions
WHERE date_livraison_reelle IS NOT NULL
  AND date_expedition IS NOT NULL
  AND date_livraison_reelle < date_expedition;

-- 6. KPI de départ : commandes par statut
SELECT statut, COUNT(*) AS nb_commandes
FROM commandes
GROUP BY statut
ORDER BY nb_commandes DESC;

-- 7. Stock par entrepôt
SELECT e.code, e.nom, SUM(s.quantite) AS quantite_totale
FROM stocks s
JOIN entrepots e ON e.id = s.entrepot_id
GROUP BY e.code, e.nom
ORDER BY quantite_totale DESC;
