import csv

# File paths
input_file = '../Data/Raw/crew.csv'  # Input CSV file
output_file = '../Data/Raw/directors.csv'  # Output CSV file

# List to store directors
directors = []

# Read the original CSV file
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)  # Read rows as dictionaries
    for row in reader:
        if row['role'] == 'Director':  # Filter only directors
            directors.append({'id': row['id'], 'name': row['name']})  # Save id and name

# Write new CSV file with only directors
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['id', 'name'])  # Define columns
    writer.writeheader()  # Write column headers
    writer.writerows(directors)  # Write director rows

print(f"Creato il file {output_file} con {len(directors)} director.")  # Confirm result
