#!/usr/bin/env python3
"""Scrape le portail web de suivi transporteur."""

from pathlib import Path
import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dataset" / "output" / "transport_portal.json"

PORTAL_BASE_URL = os.getenv(
    "TRANSFLOW_PORTAL_URL",
    "http://127.0.0.1:5050",
)

LIST_URL = f"{PORTAL_BASE_URL}/portail-transporteur/colis"


def get_soup(url: str) -> BeautifulSoup:
    """Télécharge une page HTML et retourne son arbre BeautifulSoup."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_tracking_numbers(soup: BeautifulSoup) -> list[str]:
    """Extrait les numéros de tracking depuis la liste du portail."""
    tracking_numbers = []

    for link in soup.find_all("a"):
        href = link.get("href", "")
        prefix = "/portail-transporteur/colis/"

        if href.startswith(prefix):
            tracking_number = href[len(prefix):].strip()

            if tracking_number and tracking_number not in tracking_numbers:
                tracking_numbers.append(tracking_number)

    return tracking_numbers


def scrape_detail(tracking_number: str) -> dict:
    """Extrait les données d'une page détail colis."""
    url = f"{PORTAL_BASE_URL}/portail-transporteur/colis/{tracking_number}"
    soup = get_soup(url)

    data = {
        "tracking_number": tracking_number,
    }

    for row in soup.find_all("tr"):
        cells = row.find_all(["th", "td"])

        if len(cells) != 2:
            continue

        label = cells[0].get_text(" ", strip=True)
        value = cells[1].get_text(" ", strip=True)

        mapping = {
            "Statut": "statut",
            "Adresse de livraison": "adresse_livraison",
            "Heure estimee": "heure_estimee",
            "Heure reelle": "heure_reelle",
            "Tournee": "tournee_id",
        }

        field = mapping.get(label)

        if field:
            data[field] = value

    return data


def main():
    """Collecte les colis exposés par le portail."""
    list_soup = get_soup(LIST_URL)
    tracking_numbers = extract_tracking_numbers(list_soup)

    colis = [
        scrape_detail(tracking_number)
        for tracking_number in tracking_numbers
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "source": LIST_URL,
        "nombre_colis_exposes": len(colis),
        "colis": colis,
    }

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Scraping terminé : {OUTPUT}")
    print(f"Colis exposés par le portail : {len(colis)}")


if __name__ == "__main__":
    main()