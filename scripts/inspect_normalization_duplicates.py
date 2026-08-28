from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "dataset" / "data" / "clients_fichiers"


FILES = {
    "NordDrive": ("norddrive_commandes.csv", ";"),
    "FreshMarket": ("freshmarket_commandes.csv", ","),
    "MedioTex": ("mediotex_commandes.csv", ","),
}


def normalize_date(series):
    return pd.to_datetime(
        series,
        format="mixed",
        dayfirst=True,
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")


def normalize_source(source, filename, separator):
    path = INPUT_DIR / filename

    df = pd.read_csv(
        path,
        sep=separator,
        dtype=str,
    ).drop_duplicates()

    if source == "NordDrive":
        return pd.DataFrame({
            "source": source,
            "reference_commande": df["ref_commande"],
            "date_commande": normalize_date(df["date_cde"]),
            "reference_produit": df["reference_piece"],
            "designation_produit": df["designation"],
            "quantite": pd.to_numeric(df["qte"], errors="coerce"),
            "entrepot_destination": df["entrepot"],
            "poids_unitaire_g": pd.to_numeric(
                df["poids_unitaire_g"],
                errors="coerce",
            ),
            "chaine_froid_requise": pd.NA,
        })

    if source == "FreshMarket":
        return pd.DataFrame({
            "source": source,
            "reference_commande": df["id_commande_client"],
            "date_commande": normalize_date(df["date_reception"]),
            "reference_produit": df["code_article"],
            "designation_produit": df["libelle_produit"],
            "quantite": pd.to_numeric(
                df["quantite_commandee"],
                errors="coerce",
            ),
            "entrepot_destination": df["site_livraison"],
            "poids_unitaire_g": pd.NA,
            "chaine_froid_requise": df["chaine_froid_requise"],
        })

    return pd.DataFrame({
        "source": source,
        "reference_commande": df["numero_cde"],
        "date_commande": normalize_date(df["date"]),
        "reference_produit": df["sku"],
        "designation_produit": df["description"],
        "quantite": pd.to_numeric(
            df["quantite"],
            errors="coerce",
        ),
        "entrepot_destination": df["entrepot_destination"],
        "poids_unitaire_g": pd.NA,
        "chaine_froid_requise": pd.NA,
    })


def main():
    frames = []

    for source, (filename, separator) in FILES.items():
        frames.append(
            normalize_source(
                source,
                filename,
                separator,
            )
        )

    consolidated = pd.concat(
        frames,
        ignore_index=True,
    )

    duplicated = consolidated[
        consolidated.duplicated(keep=False)
    ].sort_values(
        [
            "source",
            "reference_commande",
            "date_commande",
            "reference_produit",
        ]
    )

    print("=" * 70)
    print("DOUBLONS CREES APRES NORMALISATION")
    print("=" * 70)

    print(f"Lignes concernées : {len(duplicated)}")
    print()

    if duplicated.empty:
        print("Aucun doublon.")
        return

    print(
        duplicated.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()