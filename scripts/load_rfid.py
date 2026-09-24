#!/usr/bin/env python3
"""Importe les scans RFID JSON dans PostgreSQL."""

from pathlib import Path
import json

import psycopg
from dotenv import load_dotenv
import os


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "dataset" / "data" / "iot" / "rfid_scans.json"

conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB", "omega"),
    user=os.getenv("POSTGRES_USER", "omega"),
    password=os.getenv("POSTGRES_PASSWORD", "omega_dev_password"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)

data = json.loads(INPUT.read_text(encoding="utf-8"))

with conn:
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO iot_rfid_scans (
                scan_id,
                timestamp,
                palette_id,
                entrepot,
                zone,
                produit_sku
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            [
                (
                    row["scan_id"],
                    row["timestamp"],
                    row["palette_id"],
                    row["entrepot"],
                    row["zone"],
                    row["produit_sku"],
                )
                for row in data
            ],
        )

print(f"Import RFID terminé : {len(data)} lignes")
