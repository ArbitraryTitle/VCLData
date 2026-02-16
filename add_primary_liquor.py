#!/usr/bin/env python3
import json
import csv

# primary liquor for each cocktail
# using broad categories: vodka, whiskey, gin, tequila, rum, brandy, other
cocktail_liquors = {
    'Sazerac': 'whiskey',  # rye or cognac historically, but rye is standard
    'Sidecar': 'brandy',
    'Rusty Nail': 'whiskey',  # scotch
    'Harvey Wallbanger': 'vodka',
    'Rum Ball': 'rum',
    'Old Fashion': 'whiskey',  # bourbon
    'Between the Sheets': 'brandy',
    'Whiskey Sour': 'whiskey',
    'Negroni': 'gin',
    'Bloody Mary': 'vodka',
    'Stinger': 'brandy',
    'Soft Wink': 'whiskey',  # obscure but likely whiskey-based
    'The Magnificent Bastard': 'whiskey',  # likely whiskey
    'Manhattan': 'whiskey',  # rye or bourbon
    'Vieux Carre': 'whiskey',  # rye + cognac but rye is primary
    'Vodka Martini (Kangaroo)': 'vodka',
    'The Sun Also Sets': 'whiskey',  # likely whiskey-based
    'Moscow Mule': 'vodka',
    'The Aviation': 'gin',
    'Black Russian': 'vodka',
    'Black Ginger': 'whiskey',  # likely whiskey
    'Old Pal': 'whiskey',  # rye
    'Hemingway Daiquiri': 'rum',
    'The Packie': 'whiskey',  # likely whiskey
    'The Scofflaw': 'whiskey',  # rye
    'Hurricane': 'rum',
    'Dark & Stormy': 'rum',
    'The Kentucky Buck': 'whiskey',  # bourbon
    'Harvest Moon Old-Fashioned': 'whiskey',
    'French 75': 'gin',
    'Ward 8': 'whiskey',  # rye
    "Bourbon Tasting – Beam's Choice Collector's Edition 50+; Carleton Tower 50+; Woodford Reserve Double Oaked": 'whiskey',
    'Balvenie 14 Year Old Caribbean Cask Single Malt Scotch': 'whiskey',
    'Martinez': 'gin',
    'El Presidente': 'rum',
    'The Penicillin': 'whiskey',  # scotch
    'Blood + Sand': 'whiskey',  # scotch
    '81 Old Fashion': 'whiskey',
    'Toronto': 'whiskey',  # rye
    'Tuxedo No. 2': 'gin',
    'Brown Derby': 'whiskey',  # bourbon
    'Painkiller': 'rum',
    'Stone Fence': 'whiskey',  # colonial era, typically whiskey or rum
    'Cynar Flip': 'other',  # amaro-based
    'Paloma': 'tequila',
    'The Clover Club': 'gin',
    'The New Fashioned': 'whiskey',
    "Eric's Fancy": 'other',  # custom, unknown
    'El Diablo': 'tequila',
    'Ginger Pear Bourbon': 'whiskey',
    'Late Night Flight': 'other',  # custom, unknown
    'Turf Club': 'gin',
    'The Cape Codder': 'vodka',
    'Gold Rush': 'whiskey',  # bourbon
    'Godfather': 'whiskey',  # scotch
    'Oaxaca Old Fashioned': 'tequila',  # mezcal/tequila
    'Remember the Maine': 'whiskey',  # rye
    'Toronto Sour': 'whiskey',  # rye
    'Blackberry Smash': 'whiskey',  # likely whiskey
    'Pendergast': 'whiskey',  # likely whiskey
    "Bubby's Barrel-Aged Manhattan - Elijah Craig Small Batch Edition": 'whiskey',
    'Division Bell': 'tequila'  # mezcal
}

# load existing data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# add primary liquor column
for entry in data:
    cocktail_name = entry['cocktail']
    if cocktail_name in cocktail_liquors:
        entry['primary_liquor'] = cocktail_liquors[cocktail_name]
    else:
        entry['primary_liquor'] = 'other'
        print(f"Warning: No liquor data for '{cocktail_name}'")

# save updated json
with open('cocktail_history.json', 'w') as f:
    json.dump(data, f, indent=2)

# save updated csv
with open('cocktail_history.csv', 'w', newline='') as f:
    fieldnames = ['meeting_number', 'date', 'host', 'cocktail', 'country_of_origin', 'city_of_origin', 'primary_liquor']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"\nupdated {len(data)} cocktails with primary liquor")

# count by liquor type
from collections import Counter
liquor_counts = Counter(entry['primary_liquor'] for entry in data)
print("\nliquor distribution:")
for liquor, count in liquor_counts.most_common():
    print(f"  {liquor}: {count}")

print("\nsample entries:")
for entry in data[:5]:
    print(f"{entry['cocktail']}: {entry['primary_liquor']}")
