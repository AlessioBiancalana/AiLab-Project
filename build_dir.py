import csv

# Percorsi dei file
input_file = 'data/raw/crew.csv'
output_file = 'directors.csv'

# Lista per salvare i director
directors = []

# Leggi il file CSV originale
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if row['role'] == 'Director':
            directors.append({'id': row['id'], 'name': row['name']})

# Scrivi il nuovo CSV con solo i director
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['id', 'name'])
    writer.writeheader()
    writer.writerows(directors)

print(f"Creato il file {output_file} con {len(directors)} director.")
