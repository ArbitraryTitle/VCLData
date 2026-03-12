#!/usr/bin/env python3
import json
import csv

# Read existing album data
with open('Music/Data/vcl_albums.json', 'r') as f:
    albums = json.load(f)

# New albums to add from meetings 65-68
new_albums = [
    # Meeting 65 (6/12/2025) - Chris
    {
        "meeting_number": 65,
        "meeting_date": "6/12/2025",
        "presenter": "Chris",
        "album_position": "warm-up",
        "artist": "A Certain Ratio",
        "album_title": "To Each...",
        "release_year": 2010,
        "label": "Mute",
        "genre": "Post-Punk",
        "nation_of_origin": "UK",
        "city_of_origin": "Manchester, England",
        "micro_genre": "Dance-Punk, Funk-Punk",
        "release_date": "2010-08-10"
    },
    {
        "meeting_number": 65,
        "meeting_date": "6/12/2025",
        "presenter": "Chris",
        "album_position": "warm-up",
        "artist": "Joy Division",
        "album_title": "Closer",
        "release_year": 1980,
        "label": "Factory",
        "genre": "Post-Punk",
        "nation_of_origin": "UK",
        "city_of_origin": "Manchester, England",
        "micro_genre": "Gothic Rock, Art Punk",
        "release_date": "1980-07-18"
    },
    {
        "meeting_number": 65,
        "meeting_date": "6/12/2025",
        "presenter": "Chris",
        "album_position": "headliner",
        "artist": "Beach Boys",
        "album_title": "Pet Sounds",
        "release_year": 1966,
        "label": "Capitol",
        "genre": "Pop Rock",
        "nation_of_origin": "USA",
        "city_of_origin": "Hawthorne, California",
        "micro_genre": "Baroque Pop, Psychedelic Pop",
        "release_date": "1966-05-16"
    },
    # Meeting 66 (9/11/2025) - Joe
    {
        "meeting_number": 66,
        "meeting_date": "9/11/2025",
        "presenter": "Joe",
        "album_position": "warm-up",
        "artist": "Tyler Childers",
        "album_title": "Live on Red Barn Radio I and II",
        "release_year": 2018,
        "label": "Hickman Holler",
        "genre": "Country",
        "nation_of_origin": "USA",
        "city_of_origin": "Lawrence County, Kentucky",
        "micro_genre": "Americana, Outlaw Country",
        "release_date": "2018-07-27"
    },
    {
        "meeting_number": 66,
        "meeting_date": "9/11/2025",
        "presenter": "Joe",
        "album_position": "warm-up",
        "artist": "Imelda May",
        "album_title": "Love Tattoo",
        "release_year": 2009,
        "label": "Ambassador",
        "genre": "Rockabilly",
        "nation_of_origin": "Ireland",
        "city_of_origin": "Dublin, Ireland",
        "micro_genre": "Blues, Jazz",
        "release_date": "2009-03-23"
    },
    {
        "meeting_number": 66,
        "meeting_date": "9/11/2025",
        "presenter": "Joe",
        "album_position": "headliner",
        "artist": "Stone Temple Pilots",
        "album_title": "Purple",
        "release_year": 1994,
        "label": "Atlantic",
        "genre": "Alternative Rock",
        "nation_of_origin": "USA",
        "city_of_origin": "San Diego, California",
        "micro_genre": "Grunge, Hard Rock",
        "release_date": "1994-06-07"
    },
    # Meeting 67 (11/13/2025) - John
    {
        "meeting_number": 67,
        "meeting_date": "11/13/2025",
        "presenter": "John",
        "album_position": "warm-up",
        "artist": "Patti Smith",
        "album_title": "Horses",
        "release_year": 1975,
        "label": "Arista",
        "genre": "Punk Rock",
        "nation_of_origin": "USA",
        "city_of_origin": "New York, New York",
        "micro_genre": "Proto-Punk, Art Rock",
        "release_date": "1975-12-13"
    },
    {
        "meeting_number": 67,
        "meeting_date": "11/13/2025",
        "presenter": "John",
        "album_position": "warm-up",
        "artist": "Sinéad O'Connor",
        "album_title": "The Lion and the Cobra",
        "release_year": 1987,
        "label": "Ensign/Chrysalis",
        "genre": "Alternative Rock",
        "nation_of_origin": "Ireland",
        "city_of_origin": "Dublin, Ireland",
        "micro_genre": "Art Rock, Post-Punk",
        "release_date": "1987-11-04"
    },
    {
        "meeting_number": 67,
        "meeting_date": "11/13/2025",
        "presenter": "John",
        "album_position": "headliner",
        "artist": "Liz Phair",
        "album_title": "Exile in Guyville",
        "release_year": 1993,
        "label": "Matador",
        "genre": "Indie Rock",
        "nation_of_origin": "USA",
        "city_of_origin": "Chicago, Illinois",
        "micro_genre": "Lo-Fi, Alternative Rock",
        "release_date": "1993-06-22"
    },
    # Meeting 68 (1/8/2026) - Adam
    {
        "meeting_number": 68,
        "meeting_date": "1/8/2026",
        "presenter": "Adam",
        "album_position": "warm-up",
        "artist": "Boots",
        "album_title": "AQUΛRIA",
        "release_year": 2015,
        "label": "Columbia",
        "genre": "R&B",
        "nation_of_origin": "USA",
        "city_of_origin": "Los Angeles, California",
        "micro_genre": "Alternative R&B, Experimental",
        "release_date": "2015-11-13"
    },
    {
        "meeting_number": 68,
        "meeting_date": "1/8/2026",
        "presenter": "Adam",
        "album_position": "warm-up",
        "artist": "Balthazar",
        "album_title": "Rats",
        "release_year": 2012,
        "label": "Munich",
        "genre": "Indie Rock",
        "nation_of_origin": "Belgium",
        "city_of_origin": "Kortrijk, Belgium",
        "micro_genre": "Indie Pop, Alternative Rock",
        "release_date": "2012-10-15"
    },
    {
        "meeting_number": 68,
        "meeting_date": "1/8/2026",
        "presenter": "Adam",
        "album_position": "headliner",
        "artist": "The Temper Trap",
        "album_title": "Conditions",
        "release_year": 2009,
        "label": "Liberation/Infectious",
        "genre": "Indie Rock",
        "nation_of_origin": "Australia",
        "city_of_origin": "Melbourne, Australia",
        "micro_genre": "Alternative Rock, Post-Punk Revival",
        "release_date": "2009-06-19"
    }
]

# Add new albums
albums.extend(new_albums)

# Write updated JSON
with open('Music/Data/vcl_albums.json', 'w', encoding='utf-8') as f:
    json.dump(albums, f, indent=2, ensure_ascii=False)

# Write updated CSV
with open('Music/Data/vcl_albums.csv', 'w', newline='', encoding='utf-8') as f:
    if albums:
        writer = csv.DictWriter(f, fieldnames=albums[0].keys())
        writer.writeheader()
        writer.writerows(albums)

print(f"Updated album database with {len(new_albums)} new albums")
print(f"Total albums: {len(albums)}")
print("\nNew albums added:")
for album in new_albums:
    print(f"  Meeting {album['meeting_number']}: {album['artist']} - {album['album_title']} ({album['presenter']})")

print("\nBreakdown by meeting:")
from collections import Counter
meeting_counts = Counter(a['meeting_number'] for a in new_albums)
for meeting in sorted(meeting_counts.keys()):
    print(f"  Meeting {meeting}: {meeting_counts[meeting]} albums")
