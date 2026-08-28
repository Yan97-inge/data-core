from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
CLIENTS_DIR = BASE_DIR / "dataset" / "data" / "clients_fichiers"

FILES = {
    "NordDrive": ("norddrive_commandes.csv", ";"),
    "FreshMarket": ("freshmarket_commandes.csv", ","),
    "MedioTex": ("mediotex_commandes.csv", ","),
}


for source, (filename, separator) in FILES.items():
    path = CLIENTS_DIR / filename

    df = pd.read_csv(
        path,
        sep=separator,
        dtype=str
    )

    duplicates = df[df.duplicated(keep=False)].copy()

    print("=" * 70)
    print(source)
    print(f"Lignes totales : {len(df)}")
    print(f"Lignes concernées par un doublon exact : {len(duplicates)}")

    if not duplicates.empty:
        print("\nExemples :")
        print(duplicates.head(10).to_string(index=False))