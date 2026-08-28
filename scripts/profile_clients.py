from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CLIENTS_DIR = BASE_DIR / "dataset" / "data" / "clients_fichiers"


FILES = {
    "NordDrive": "norddrive_commandes.csv",
    "FreshMarket": "freshmarket_commandes.csv",
    "MedioTex": "mediotex_commandes.csv",
}


def detect_separator(path):
    with path.open("r", encoding="utf-8") as f:
        header = f.readline()

    if header.count(";") > header.count(","):
        return ";"

    return ","


def profile_source(source_name, filename):
    path = CLIENTS_DIR / filename
    separator = detect_separator(path)

    df = pd.read_csv(
        path,
        sep=separator,
        dtype=str
    )

    print("=" * 70)
    print(f"SOURCE : {source_name}")
    print(f"FICHIER : {filename}")
    print(f"SEPARATEUR : {repr(separator)}")
    print(f"NOMBRE DE LIGNES : {len(df)}")
    print(f"NOMBRE DE COLONNES : {len(df.columns)}")

    print("\nCOLONNES")
    for column in df.columns:
        print(f"  - {column}")

    print("\nVALEURS MANQUANTES")
    missing = df.isna().sum()

    for column, count in missing.items():
        print(f"  - {column}: {count}")

    print(f"\nDOUBLONS COMPLETS : {df.duplicated().sum()}")

    first_column = df.columns[0]

    print(
        f"DUPLICATIONS SUR L'IDENTIFIANT "
        f"({first_column}) : {df[first_column].duplicated().sum()}"
    )

    print("\nPREMIERES VALEURS")
    print(df.head(3).to_string(index=False))

    print()


def main():
    for source_name, filename in FILES.items():
        profile_source(source_name, filename)


if __name__ == "__main__":
    main()