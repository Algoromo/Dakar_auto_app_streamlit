import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Nettoyage du prix
    if 'prix' in df.columns:
        df['prix'] = df['prix'].astype(str).str.replace('[^0-9]', '', regex=True)
        df['prix'] = pd.to_numeric(df['prix'], errors='coerce')

    # Nettoyage kilométrage
    if 'kilometrage' in df.columns:
        df['kilometrage'] = df['kilometrage'].astype(str).str.replace('[^0-9]', '', regex=True)
        df['kilometrage'] = pd.to_numeric(df['kilometrage'], errors='coerce')

    # Nettoyage année
    if 'annee' in df.columns:
        df['annee'] = df['annee'].astype(str).str.extract(r'(\d{4})')
        df['annee'] = pd.to_numeric(df['annee'], errors='coerce')

    # Valeurs manquantes
    df = df.dropna(subset=["marque", "prix"], how="any")

    return df
