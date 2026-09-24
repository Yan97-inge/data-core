CREATE TABLE IF NOT EXISTS iot_camera_comptage (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    entrepot VARCHAR(20) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    nb_passages INTEGER NOT NULL CHECK (nb_passages >= 0),
    sens VARCHAR(10) NOT NULL CHECK (sens IN ('entree', 'sortie'))
);

CREATE INDEX IF NOT EXISTS idx_iot_camera_timestamp
    ON iot_camera_comptage (timestamp);

CREATE INDEX IF NOT EXISTS idx_iot_camera_entrepot
    ON iot_camera_comptage (entrepot);


CREATE TABLE IF NOT EXISTS iot_capteurs_temperature (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    entrepot VARCHAR(20) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    temperature_c NUMERIC(5,2) NOT NULL,
    alerte SMALLINT NOT NULL CHECK (alerte IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_iot_temperature_timestamp
    ON iot_capteurs_temperature (timestamp);

CREATE INDEX IF NOT EXISTS idx_iot_temperature_entrepot
    ON iot_capteurs_temperature (entrepot);


CREATE TABLE IF NOT EXISTS iot_geoloc_flotte (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    vehicule_id VARCHAR(20) NOT NULL,
    lat NUMERIC(9,6) NOT NULL CHECK (lat BETWEEN -90 AND 90),
    lon NUMERIC(9,6) NOT NULL CHECK (lon BETWEEN -180 AND 180),
    vitesse_kmh NUMERIC(6,2) NOT NULL CHECK (vitesse_kmh >= 0)
);

CREATE INDEX IF NOT EXISTS idx_iot_geoloc_timestamp
    ON iot_geoloc_flotte (timestamp);

CREATE INDEX IF NOT EXISTS idx_iot_geoloc_vehicule
    ON iot_geoloc_flotte (vehicule_id);


CREATE TABLE IF NOT EXISTS iot_rfid_scans (
    scan_id BIGINT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    palette_id VARCHAR(30) NOT NULL,
    entrepot VARCHAR(20) NOT NULL,
    zone VARCHAR(100) NOT NULL,
    produit_sku VARCHAR(30) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_iot_rfid_timestamp
    ON iot_rfid_scans (timestamp);

CREATE INDEX IF NOT EXISTS idx_iot_rfid_palette
    ON iot_rfid_scans (palette_id);

CREATE INDEX IF NOT EXISTS idx_iot_rfid_produit
    ON iot_rfid_scans (produit_sku);
