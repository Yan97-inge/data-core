#!/usr/bin/env python3
"""Collecte des données TransFlow via l'API REST."""

from pathlib import Path
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dataset" / "output" / "transflow_api.json"

API_BASE_URL = os.getenv(
    "TRANSFLOW_API_URL",
    "http://127.0.0.1:5050/api",
)
API_KEY = os.getenv(
    "TRANSFLOW_API_KEY",
    "datacore-training-2026",
)

HEADERS = {
    "X-API-Key": API_KEY,
}


def get_json(endpoint: str):
    """Appelle un endpoint JSON de l'API TransFlow."""
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    """Collecte les ressources de l'API."""

    # Transporteurs
    transporteurs = get_json("transporteurs")

    # Tournées - première page
    premiere_page = get_json("tournees")

    tournees = {
        "page": 1,
        "per_page": premiere_page["per_page"],
        "results": premiere_page["results"],
        "total": premiere_page["total"],
        "total_pages": premiere_page["total_pages"],
    }

    # Tournées - pages suivantes
    for page in range(2, premiere_page["total_pages"] + 1):
        page_data = get_json(f"tournees?page={page}")
        tournees["results"].extend(page_data["results"])

    # Livraisons - première page
    premiere_page_livraisons = get_json("livraisons")

    livraisons = {
        "page": 1,
        "per_page": premiere_page_livraisons["per_page"],
        "results": premiere_page_livraisons["results"],
        "total": premiere_page_livraisons["total"],
        "total_pages": premiere_page_livraisons["total_pages"],
    }

    # Livraisons - pages suivantes
    for page in range(2, premiere_page_livraisons["total_pages"] + 1):
        page_data = get_json(f"livraisons?page={page}")
        livraisons["results"].extend(page_data["results"])

    # Création du dossier de sortie
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Données finales
    data = {
        "source": API_BASE_URL,
        "transporteurs": transporteurs,
        "tournees": tournees,
        "livraisons": livraisons,
    }

    # Écriture du fichier JSON
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Collecte terminée : {OUTPUT}")
    print(f"Transporteurs : {len(transporteurs)}")
    print(f"Tournées collectées : {len(tournees['results'])}")
    print(f"Total tournées API : {tournees['total']}")
    print(f"Livraisons collectées : {len(livraisons['results'])}")
    print(f"Total livraisons API : {livraisons['total']}")


if __name__ == "__main__":
    main()