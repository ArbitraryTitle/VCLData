#!/usr/bin/env python3
import json

# Read existing cocktail history
with open('Cocktail/Data/cocktail_history.json', 'r') as f:
    cocktails = json.load(f)

# New cocktails to add
new_cocktails = [
    {
        "meeting_number": 65,
        "date": "6/12/2025",
        "host": "Chris",
        "cocktail": "Paper Plane",
        "country_of_origin": "USA",
        "city_of_origin": "Chicago, Illinois",
        "primary_liquor": "whiskey",
        "whiskey_type": "bourbon",
        "year_invented": 2007
    },
    {
        "meeting_number": 66,
        "date": "9/11/2025",
        "host": "Joe",
        "cocktail": "Maple Old Fashioned",
        "country_of_origin": "USA",
        "city_of_origin": "USA",
        "primary_liquor": "whiskey",
        "whiskey_type": "bourbon",
        "year_invented": 2010
    },
    {
        "meeting_number": 67,
        "date": "11/13/2025",
        "host": "John",
        "cocktail": "Mexican Firing Squad",
        "country_of_origin": "Mexico",
        "city_of_origin": "Mexico City",
        "primary_liquor": "tequila",
        "whiskey_type": "N/A",
        "year_invented": 1937
    },
    {
        "meeting_number": 68,
        "date": "1/8/2026",
        "host": "Adam",
        "cocktail": "C&B Old Fashioned",
        "country_of_origin": "USA",
        "city_of_origin": "New York, New York",
        "primary_liquor": "gin",
        "whiskey_type": "N/A",
        "year_invented": 2011
    }
]

# Add new cocktails
cocktails.extend(new_cocktails)

# Write updated data back to file
with open('Cocktail/Data/cocktail_history.json', 'w') as f:
    json.dump(cocktails, f, indent=2)

print(f"Updated cocktail history with {len(new_cocktails)} new entries")
print(f"Total entries: {len(cocktails)}")
print("\nNew entries added:")
for cocktail in new_cocktails:
    print(f"  Meeting {cocktail['meeting_number']}: {cocktail['cocktail']} ({cocktail['host']})")
