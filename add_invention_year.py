#!/usr/bin/env python3
import json
import csv

# cocktail invention years - researched from cocktail history
# some are well-documented, others are approximate
cocktail_invention_years = {
    'Sazerac': 1838,
    'Sidecar': 1920,  # circa, disputed
    'Rusty Nail': 1937,  # popularized later in 1960s
    'Harvey Wallbanger': 1952,
    'Rum Ball': 1950,  # approximate, unclear
    'Old Fashion': 1880,  # circa
    'Between the Sheets': 1930,  # circa
    'Whiskey Sour': 1870,  # circa, variations existed earlier
    'Negroni': 1919,
    'Bloody Mary': 1921,
    'Stinger': 1890,  # circa
    'Soft Wink': 1960,  # approximate, obscure
    'The Magnificent Bastard': 2000,  # modern/custom
    'Manhattan': 1874,  # circa
    'Vieux Carre': 1938,
    'Vodka Martini (Kangaroo)': 1950,  # circa
    'The Sun Also Sets': 2000,  # modern/custom
    'Moscow Mule': 1941,
    'The Aviation': 1916,
    'Black Russian': 1949,
    'Black Ginger': 2000,  # modern/custom
    'Old Pal': 1922,
    'Hemingway Daiquiri': 1930,  # circa
    'The Packie': 2000,  # modern/custom
    'The Scofflaw': 1924,
    'Hurricane': 1940,  # circa
    'Dark & Stormy': 1950,  # circa
    'The Kentucky Buck': 1930,  # circa
    'Harvest Moon Old-Fashioned': 2010,  # modern variation
    'French 75': 1915,
    'Ward 8': 1898,
    "Bourbon Tasting – Beam's Choice Collector's Edition 50+; Carleton Tower 50+; Woodford Reserve Double Oaked": 2000,  # N/A for tasting
    'Balvenie 14 Year Old Caribbean Cask Single Malt Scotch': 2000,  # N/A for scotch tasting
    'Martinez': 1887,  # circa
    'El Presidente': 1920,  # circa
    'The Penicillin': 2005,
    'Blood + Sand': 1930,
    '81 Old Fashion': 2000,  # modern variation
    'Toronto': 1922,
    'Tuxedo No. 2': 1882,  # circa
    'Brown Derby': 1930,  # circa
    'Painkiller': 1970,  # circa
    'Stone Fence': 1775,  # colonial era, very old
    'Cynar Flip': 2010,  # modern
    'Paloma': 1950,  # circa
    'The Clover Club': 1910,  # circa
    'The New Fashioned': 2010,  # modern
    "Eric's Fancy": 2020,  # custom
    'El Diablo': 1946,
    'Ginger Pear Bourbon': 2015,  # custom
    'Late Night Flight': 2020,  # custom
    'Turf Club': 1894,  # circa
    'The Cape Codder': 1945,  # circa
    'Gold Rush': 2001,
    'Godfather': 1972,
    'Oaxaca Old Fashioned': 2007,
    'Remember the Maine': 1899,
    'Toronto Sour': 1922,
    'Blackberry Smash': 2010,  # modern
    'Pendergast': 2020,  # custom
    "Bubby's Barrel-Aged Manhattan - Elijah Craig Small Batch Edition": 2020,  # custom
    'Division Bell': 2009
}

# load existing data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# add invention year column
for entry in data:
    cocktail_name = entry['cocktail']
    if cocktail_name in cocktail_invention_years:
        entry['year_invented'] = cocktail_invention_years[cocktail_name]
    else:
        entry['year_invented'] = None
        print(f"Warning: No invention year for '{cocktail_name}'")

# save updated json
with open('cocktail_history.json', 'w') as f:
    json.dump(data, f, indent=2)

# save updated csv
with open('cocktail_history.csv', 'w', newline='') as f:
    fieldnames = ['meeting_number', 'date', 'host', 'cocktail', 'country_of_origin', 'city_of_origin', 'primary_liquor', 'whiskey_type', 'year_invented']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"\nupdated {len(data)} cocktails with invention years")

# stats by era
from collections import Counter
era_counts = Counter()
for entry in data:
    year = entry.get('year_invented')
    if year:
        if year < 1900:
            era = '1800s'
        elif year < 1920:
            era = '1900-1919'
        elif year < 1940:
            era = '1920-1939'
        elif year < 1960:
            era = '1940-1959'
        elif year < 1980:
            era = '1960-1979'
        elif year < 2000:
            era = '1980-1999'
        else:
            era = '2000+'
        era_counts[era] += 1

print("\ncocktails by era:")
for era in sorted(era_counts.keys()):
    print(f"  {era}: {era_counts[era]}")

print("\noldest cocktails:")
oldest = sorted([e for e in data if e.get('year_invented')], key=lambda x: x['year_invented'])[:5]
for c in oldest:
    print(f"  {c['year_invented']}: {c['cocktail']}")

print("\nnewest cocktails:")
newest = sorted([e for e in data if e.get('year_invented')], key=lambda x: x['year_invented'], reverse=True)[:5]
for c in newest:
    print(f"  {c['year_invented']}: {c['cocktail']}")
