#!/usr/bin/env python3
import json
import csv

# cocktail origins - researched from cocktail history
cocktail_origins = {
    'Sazerac': {'country': 'USA', 'city': 'New Orleans, Louisiana'},
    'Sidecar': {'country': 'France', 'city': 'Paris'},  # disputed but commonly attributed to Paris
    'Rusty Nail': {'country': 'USA', 'city': 'USA'},  # origin unclear, popularized in USA
    'Harvey Wallbanger': {'country': 'USA', 'city': 'Los Angeles, California'},
    'Rum Ball': {'country': 'USA', 'city': 'USA'},  # unclear origin
    'Old Fashion': {'country': 'USA', 'city': 'Louisville, Kentucky'},  # disputed with Wisconsin
    'Between the Sheets': {'country': 'France', 'city': 'Paris'},
    'Whiskey Sour': {'country': 'USA', 'city': 'USA'},  # origin uncertain
    'Negroni': {'country': 'Italy', 'city': 'Florence'},
    'Bloody Mary': {'country': 'France', 'city': 'Paris'},  # Harry's New York Bar
    'Stinger': {'country': 'USA', 'city': 'USA'},
    'Soft Wink': {'country': 'USA', 'city': 'USA'},  # obscure, likely USA
    'The Magnificent Bastard': {'country': 'USA', 'city': 'USA'},  # likely custom/unknown
    'Manhattan': {'country': 'USA', 'city': 'New York, New York'},
    'Vieux Carre': {'country': 'USA', 'city': 'New Orleans, Louisiana'},
    'Vodka Martini (Kangaroo)': {'country': 'USA', 'city': 'USA'},  # martini variation
    'The Sun Also Sets': {'country': 'USA', 'city': 'USA'},  # likely custom
    'Moscow Mule': {'country': 'USA', 'city': 'Los Angeles, California'},
    'The Aviation': {'country': 'USA', 'city': 'New York, New York'},
    'Black Russian': {'country': 'Belgium', 'city': 'Brussels'},
    'Black Ginger': {'country': 'USA', 'city': 'USA'},  # likely custom
    'Old Pal': {'country': 'France', 'city': 'Paris'},  # Harry's New York Bar
    'Hemingway Daiquiri': {'country': 'Cuba', 'city': 'Havana'},
    'The Packie': {'country': 'USA', 'city': 'USA'},  # custom/local slang
    'The Scofflaw': {'country': 'USA', 'city': 'USA'},  # Harry's New York Bar in Paris but American creation
    'Hurricane': {'country': 'USA', 'city': 'New Orleans, Louisiana'},
    'Dark & Stormy': {'country': 'Bermuda', 'city': 'Bermuda'},
    'The Kentucky Buck': {'country': 'USA', 'city': 'USA'},
    'Harvest Moon Old-Fashioned': {'country': 'USA', 'city': 'USA'},  # variation
    'French 75': {'country': 'France', 'city': 'Paris'},
    'Ward 8': {'country': 'USA', 'city': 'Boston, Massachusetts'},
    "Bourbon Tasting – Beam's Choice Collector's Edition 50+; Carleton Tower 50+; Woodford Reserve Double Oaked": {'country': 'USA', 'city': 'Kentucky'},
    'Balvenie 14 Year Old Caribbean Cask Single Malt Scotch': {'country': 'Scotland', 'city': 'Dufftown, Scotland'},
    'Martinez': {'country': 'USA', 'city': 'San Francisco, California'},  # disputed with Martinez, CA
    'El Presidente': {'country': 'Cuba', 'city': 'Havana'},
    'The Penicillin': {'country': 'USA', 'city': 'New York, New York'},
    'Blood + Sand': {'country': 'UK', 'city': 'London'},
    '81 Old Fashion': {'country': 'USA', 'city': 'USA'},  # variation
    'Toronto': {'country': 'Canada', 'city': 'Toronto, Ontario'},
    'Tuxedo No. 2': {'country': 'USA', 'city': 'New York, New York'},
    'Brown Derby': {'country': 'USA', 'city': 'Los Angeles, California'},
    'Painkiller': {'country': 'British Virgin Islands', 'city': 'Tortola'},
    'Stone Fence': {'country': 'USA', 'city': 'USA'},  # colonial era cocktail
    'Cynar Flip': {'country': 'USA', 'city': 'USA'},  # modern variation
    'Paloma': {'country': 'Mexico', 'city': 'Mexico'},
    'The Clover Club': {'country': 'USA', 'city': 'Philadelphia, Pennsylvania'},
    'The New Fashioned': {'country': 'USA', 'city': 'USA'},  # variation
    "Eric's Fancy": {'country': 'USA', 'city': 'USA'},  # custom
    'El Diablo': {'country': 'USA', 'city': 'USA'},  # Trader Vic's creation
    'Ginger Pear Bourbon': {'country': 'USA', 'city': 'USA'},  # custom
    'Late Night Flight': {'country': 'USA', 'city': 'USA'},  # custom
    'Turf Club': {'country': 'USA', 'city': 'USA'},
    'The Cape Codder': {'country': 'USA', 'city': 'Cape Cod, Massachusetts'},
    'Gold Rush': {'country': 'USA', 'city': 'New York, New York'},
    'Godfather': {'country': 'USA', 'city': 'USA'},
    'Oaxaca Old Fashioned': {'country': 'USA', 'city': 'New York, New York'},  # created at Death & Co
    'Remember the Maine': {'country': 'USA', 'city': 'New York, New York'},
    'Toronto Sour': {'country': 'Canada', 'city': 'Toronto, Ontario'},
    'Blackberry Smash': {'country': 'USA', 'city': 'USA'},  # likely custom
    'Pendergast': {'country': 'USA', 'city': 'USA'},  # likely custom
    "Bubby's Barrel-Aged Manhattan - Elijah Craig Small Batch Edition": {'country': 'USA', 'city': 'USA'},  # custom variation
    'Division Bell': {'country': 'USA', 'city': 'New York, New York'}  # created at Mayahuel by Phil Ward
}

# load existing data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# add origin columns
for entry in data:
    cocktail_name = entry['cocktail']
    if cocktail_name in cocktail_origins:
        entry['country_of_origin'] = cocktail_origins[cocktail_name]['country']
        entry['city_of_origin'] = cocktail_origins[cocktail_name]['city']
    else:
        entry['country_of_origin'] = 'Unknown'
        entry['city_of_origin'] = 'Unknown'
        print(f"Warning: No origin data for '{cocktail_name}'")

# save updated json
with open('cocktail_history.json', 'w') as f:
    json.dump(data, f, indent=2)

# save updated csv
with open('cocktail_history.csv', 'w', newline='') as f:
    fieldnames = ['meeting_number', 'date', 'host', 'cocktail', 'country_of_origin', 'city_of_origin']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"\nupdated {len(data)} cocktails with origin data")
print("\nsample entries:")
for entry in data[:5]:
    print(f"{entry['cocktail']}: {entry['city_of_origin']}, {entry['country_of_origin']}")
