#!/usr/bin/env python3
import json
import csv

# whiskey types for whiskey-based cocktails
whiskey_types = {
    'Sazerac': 'rye',
    'Rusty Nail': 'scotch',
    'Old Fashion': 'bourbon',
    'Whiskey Sour': 'bourbon',  # typically bourbon, though generic
    'The Magnificent Bastard': 'whiskey',  # unknown type
    'Manhattan': 'rye',  # traditionally rye, though bourbon also common
    'Vieux Carre': 'rye',  # rye + cognac but rye primary
    'Soft Wink': 'whiskey',  # unknown
    'The Sun Also Sets': 'whiskey',  # unknown
    'Black Ginger': 'whiskey',  # unknown
    'Old Pal': 'rye',
    'The Packie': 'whiskey',  # unknown
    'The Scofflaw': 'rye',
    'The Kentucky Buck': 'bourbon',
    'Harvest Moon Old-Fashioned': 'bourbon',
    'Ward 8': 'rye',
    "Bourbon Tasting – Beam's Choice Collector's Edition 50+; Carleton Tower 50+; Woodford Reserve Double Oaked": 'bourbon',
    'Balvenie 14 Year Old Caribbean Cask Single Malt Scotch': 'scotch',
    'The Penicillin': 'scotch',
    'Blood + Sand': 'scotch',
    '81 Old Fashion': 'bourbon',
    'Toronto': 'rye',
    'Brown Derby': 'bourbon',
    'Stone Fence': 'whiskey',  # colonial era, varies
    'The New Fashioned': 'bourbon',
    'Ginger Pear Bourbon': 'bourbon',
    'Gold Rush': 'bourbon',
    'Godfather': 'scotch',
    'Remember the Maine': 'rye',
    'Toronto Sour': 'rye',
    'Blackberry Smash': 'bourbon',  # likely
    'Pendergast': 'whiskey',  # unknown
    "Bubby's Barrel-Aged Manhattan - Elijah Craig Small Batch Edition": 'bourbon'  # Elijah Craig is bourbon
}

# load existing data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# add whiskey type column
for entry in data:
    cocktail_name = entry['cocktail']
    if entry['primary_liquor'] == 'whiskey':
        if cocktail_name in whiskey_types:
            entry['whiskey_type'] = whiskey_types[cocktail_name]
        else:
            entry['whiskey_type'] = 'whiskey'  # generic/unknown
            print(f"Warning: No whiskey type for '{cocktail_name}'")
    else:
        entry['whiskey_type'] = 'N/A'

# save updated json
with open('cocktail_history.json', 'w') as f:
    json.dump(data, f, indent=2)

# save updated csv
with open('cocktail_history.csv', 'w', newline='') as f:
    fieldnames = ['meeting_number', 'date', 'host', 'cocktail', 'country_of_origin', 'city_of_origin', 'primary_liquor', 'whiskey_type']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"\nupdated {len(data)} cocktails with whiskey types")

# count whiskey types
from collections import Counter
whiskey_entries = [e for e in data if e['primary_liquor'] == 'whiskey']
whiskey_type_counts = Counter(entry['whiskey_type'] for entry in whiskey_entries)
print(f"\nwhiskey breakdown (n={len(whiskey_entries)}):")
for wtype, count in whiskey_type_counts.most_common():
    print(f"  {wtype}: {count}")

print("\nsample whiskey entries:")
for entry in [e for e in data if e['primary_liquor'] == 'whiskey'][:5]:
    print(f"{entry['cocktail']}: {entry['whiskey_type']}")
