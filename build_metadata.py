import os
import pandas as pd

# === 1. Percorsi e costanti ===
RAW_DIR = "data/raw"
POSTER_DIR = "data/posters"
OUTPUT_FILE = "data/metadata.csv"
LIMIT = 300  # massimo numero di film

# === 2. Caricamento file CSV ===
movies = pd.read_csv(os.path.join(RAW_DIR, "movies.csv"))      # id, name, date, minute, description, rating
genres = pd.read_csv(os.path.join(RAW_DIR, "genres.csv"))      # id, genre
actors = pd.read_csv(os.path.join(RAW_DIR, "actors.csv"))      # id, actor
studios = pd.read_csv(os.path.join(RAW_DIR, "studios.csv"))    # id, studio

# === 3. Raggruppamento dei generi per film ===
genres_grouped = genres.groupby("id")["genre"] \
    .apply(lambda g: "|".join(sorted(set(g)))) \
    .reset_index() \
    .rename(columns={"id": "id", "genre": "genres"})

# === 4. Raggruppamento del cast per film ===
actors_grouped = actors.groupby("id")["name"] \
    .apply(lambda a: ", ".join(a.dropna().astype(str))) \
    .reset_index() \
    .rename(columns={"name": "cast"})

# === 5. Raggruppamento dello studio per film ===
studios_grouped = studios.groupby("id")["studio"] \
    .apply(lambda s: "|".join(sorted(set(s.dropna().astype(str))))) \
    .reset_index() \
    .rename(columns={"id": "id", "studio": "studio"})

# === 6. Preparazione del DataFrame film ===
df = movies.rename(columns={
    "id": "id",
    "name": "title",
    "date": "year",
    "minute": "duration",
    "description": "description",
    "rating": "rating"
})[["id", "title", "year", "duration", "description", "rating"]]

# === 7. Merge con generi, cast, studio ===
df = df.merge(genres_grouped, on="id", how="left")
df = df.merge(actors_grouped, on="id", how="left")
df = df.merge(studios_grouped, on="id", how="left")

# === 8. Aggiunta colonna con path ai poster ===
df["poster_path"] = df["id"].apply(lambda i: os.path.join("data/posters", f"{i}.jpg"))

# === 9. Filtro: includi solo film con immagine esistente ===
df = df[df["poster_path"].apply(os.path.exists)]

# === 10. Limita ai primi N film ===
df = df.head(LIMIT)

# === 11. Salvataggio finale ===
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ metadata.csv creato con successo: {len(df)} film inclusi.")
