#!/usr/bin/env python3
"""Recharge les 7 CSV FluxPro dans PostgreSQL.

Usage:
  python scripts/load_fluxpro.py

Variables .env supportées:
  POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
"""

from pathlib import Path
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset" / "data"

TABLES = [
    ("entrepots", "entrepots.csv"),
    ("clients", "clients.csv"),
    ("produits", "produits.csv"),
    ("commandes", "commandes.csv"),
    ("lignes_commande", "lignes_commande.csv"),
    ("expeditions", "expeditions.csv"),
    ("stocks", "stocks.csv"),
]


def main():
    conninfo = {
        "dbname": os.getenv("POSTGRES_DB", "omega"),
        "user": os.getenv("POSTGRES_USER", "omega"),
        "password": os.getenv("POSTGRES_PASSWORD", "omega_dev_password"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }

    with psycopg.connect(**conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                TRUNCATE TABLE
                    stocks,
                    expeditions,
                    lignes_commande,
                    commandes,
                    produits,
                    entrepots,
                    clients
                RESTART IDENTITY CASCADE
                """
            )

            for table, filename in TABLES:
                path = DATA / filename

                with path.open("r", encoding="utf-8") as f:
                    with cur.copy(
                        f"COPY {table} FROM STDIN WITH "
                        f"(FORMAT csv, HEADER true, DELIMITER ',')"
                    ) as copy:
                        while data := f.read(1024 * 1024):
                            copy.write(data)

                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"{table:20s} -> {count:>6} lignes")

        conn.commit()


if __name__ == "__main__":
    main()
