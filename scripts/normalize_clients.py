from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = BASE_DIR / "dataset" / "data" / "clients_fichiers"
OUTPUT_DIR = BASE_DIR / "dataset" / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_date(series):
    """
    Convertit les différents formats de date vers YYYY-MM-DD.
    Les dates invalides deviennent NaT.
    """
    return pd.to_datetime(
        series,
        format="mixed",
        dayfirst=True,
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")


def normalize_norddrive():
    path = INPUT_DIR / "norddrive_commandes.csv"

    df = pd.read_csv(
        path,
        sep=";",
        dtype=str,
    )

    df = df.drop_duplicates().copy()

    result = pd.DataFrame(
        {
            "source": "NordDrive",
            "reference_commande": df["ref_commande"],
            "date_commande": normalize_date(df["date_cde"]),
            "reference_produit": df["reference_piece"],
            "designation_produit": df["designation"],
            "quantite": pd.to_numeric(
                df["qte"],
                errors="coerce",
            ),
            "entrepot_destination": df["entrepot"],
            "poids_unitaire_g": pd.to_numeric(
                df["poids_unitaire_g"],
                errors="coerce",
            ),
            "chaine_froid_requise": pd.NA,
        }
    )

    return result


def normalize_freshmarket():
    path = INPUT_DIR / "freshmarket_commandes.csv"

    df = pd.read_csv(
        path,
        sep=",",
        dtype=str,
    )

    df = df.drop_duplicates().copy()

    result = pd.DataFrame(
        {
            "source": "FreshMarket",
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
        }
    )

    return result


def normalize_mediotex():
    path = INPUT_DIR / "mediotex_commandes.csv"

    df = pd.read_csv(
        path,
        sep=",",
        dtype=str,
    )

    df = df.drop_duplicates().copy()

    result = pd.DataFrame(
        {
            "source": "MedioTex",
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
        }
    )

    return result


def main():
    norddrive = normalize_norddrive()
    freshmarket = normalize_freshmarket()
    mediotex = normalize_mediotex()

    consolidated = pd.concat(
        [
            norddrive,
            freshmarket,
            mediotex,
        ],
        ignore_index=True,
    )

    duplicates_after_normalization = consolidated.duplicated().sum()

    if duplicates_after_normalization > 0:
        print(
            f"\nDoublons créés par la normalisation : "
            f"{duplicates_after_normalization}"
        )

        consolidated = consolidated.drop_duplicates().reset_index(
            drop=True
        )

    output_file = OUTPUT_DIR / "clients_consolides.csv"

    consolidated.to_csv(
        output_file,
        index=False,
        encoding="utf-8",
    )

    print("=" * 70)
    print("NORMALISATION TERMINEE")
    print("=" * 70)

    print(f"Fichier produit : {output_file}")
    print(f"Nombre total de lignes : {len(consolidated)}")
    print(f"Nombre de colonnes : {len(consolidated.columns)}")

    print("\nLignes par source :")
    print(consolidated["source"].value_counts().sort_index())

    print("\nQuantités manquantes :")
    print(consolidated["quantite"].isna().sum())

    print("\nDates invalides/manquantes :")
    print(consolidated["date_commande"].isna().sum())

    print("\nDoublons exacts après consolidation :")
    print(consolidated.duplicated().sum())

    print("\nAperçu :")
    print(consolidated.head(10).to_string(index=False))


if __name__ == "__main__":
    main()