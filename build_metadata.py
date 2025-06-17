import os
import pandas as pd

# === 1. Paths and constants ===
RAW_DIR = "data/raw"
POSTER_DIR = "data/posters"
OUTPUT_FILE = "data/metadata.csv"
LIMIT = 300  # maximum number of movies

# === 2. Load CSV files ===
movies = pd.read_csv(os.path.join(RAW_DIR, "movies.csv"))      # id, name, date, minute, description, rating
genres = pd.read_csv(os.path.join(RAW_DIR, "genres.csv"))      # id, genre
actors = pd.read_csv(os.path.join(RAW_DIR, "actors.csv"))      # id, actor
studios = pd.read_csv(os.path.join(RAW_DIR, "studios.csv"))    # id, studio
directors = pd.read_csv(os.path.join(RAW_DIR, "directors.csv"))  # id, name

# === 3. Group genres per movie ===
genres_grouped = genres.groupby("id")["genre"] \
    .apply(lambda g: "|".join(sorted(set(g)))) \
    .reset_index() \
    .rename(columns={"id": "id", "genre": "genres"})

# === 4. Group cast per movie ===
actors_grouped = actors.groupby("id")["name"] \
    .apply(lambda a: ", ".join(a.dropna().astype(str))) \
    .reset_index() \
    .rename(columns={"name": "cast"})

# === 5. Group studios per movie ===
studios_grouped = studios.groupby("id")["studio"] \
    .apply(lambda s: "|".join(sorted(set(s.dropna().astype(str))))) \
    .reset_index() \
    .rename(columns={"id": "id", "studio": "studio"})

# === 6. Group director per movie ===
directors_grouped = directors.groupby("id")["name"] \
    .apply(lambda d: ", ".join(d.dropna().astype(str))) \
    .reset_index() \
    .rename(columns={"name": "director"})

# === 7. Prepare main movie DataFrame ===
df = movies.rename(columns={
    "id": "id",
    "name": "title",
    "date": "year",
    "minute": "duration",
    "description": "description",
    "rating": "rating"
})[["id", "title", "year", "duration", "description", "rating"]]

# === 8. Merge genres, cast, studios and director ===
df = df.merge(genres_grouped, on="id", how="left")
df = df.merge(actors_grouped, on="id", how="left")
df = df.merge(studios_grouped, on="id", how="left")
df = df.merge(directors_grouped, on="id", how="left")

# === 9. Add column with poster path ===
df["poster_path"] = df["id"].apply(lambda i: os.path.join("data/posters", f"{i}.jpg"))

# === 10. Filter: include only movies with an existing poster ===
df = df[df["poster_path"].apply(os.path.exists)]

# === 11. Limit to the first N movies ===
df = df.head(LIMIT)

# === 12. Save final metadata file ===
os.makedirs("data", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ metadata.csv successfully created: {len(df)} movies included.")
