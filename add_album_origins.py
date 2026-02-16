#!/usr/bin/env python3
import json
import csv
from collections import Counter

# load current album data
with open('vcl_albums.json', 'r') as f:
    albums = json.load(f)

# band/artist origins - manually researched
# format: artist_name: (nation, city)
artist_origins = {
    'King Crimson': ('UK', 'London'),
    'Mountain': ('USA', 'New York, New York'),
    'Sebadoh': ('USA', 'Northampton, Massachusetts'),
    'Yo La Tengo': ('USA', 'Hoboken, New Jersey'),
    'Ben Lee': ('Australia', 'Sydney'),
    'The Knife': ('Sweden', 'Gothenburg'),
    'Jefferson Airplane': ('USA', 'San Francisco, California'),
    'Talking Heads': ('USA', 'New York, New York'),
    'The Afghan Whigs': ('USA', 'Cincinnati, Ohio'),
    'The Stooges': ('USA', 'Ann Arbor, Michigan'),
    'James Brown': ('USA', 'Augusta, Georgia'),
    'Various Artists': ('Various', 'Various'),
    'Various': ('Various', 'Various'),
    'Paul Simon': ('USA', 'Newark, New Jersey'),
    'Arcade Fire': ('Canada', 'Montreal, Quebec'),
    'Vampire Weekend': ('USA', 'New York, New York'),
    'The Replacements': ('USA', 'Minneapolis, Minnesota'),
    'The Jam': ('UK', 'Woking, Surrey'),
    'Big Star': ('USA', 'Memphis, Tennessee'),
    'Joy Division': ('UK', 'Manchester'),
    'Genesis': ('UK', 'Godalming, Surrey'),
    'Radiohead': ('UK', 'Abingdon, Oxfordshire'),
    'Adrian Belew': ('USA', 'Covington, Kentucky'),
    'Robin Trower': ('UK', 'London'),
    'Santana': ('USA', 'San Francisco, California'),
    'Frightened Rabbit': ('UK', 'Selkirk, Scotland'),
    'Leonard Cohen': ('Canada', 'Montreal, Quebec'),
    'Bob Dylan': ('USA', 'Duluth, Minnesota'),
    'Galaxie 500': ('USA', 'Cambridge, Massachusetts'),
    'Morphine': ('USA', 'Cambridge, Massachusetts'),
    'Built to Spill': ('USA', 'Boise, Idaho'),
    'MC5': ('USA', 'Detroit, Michigan'),
    'Mastodon': ('USA', 'Atlanta, Georgia'),
    'Black Sabbath': ('UK', 'Birmingham'),
    'Live': ('USA', 'York, Pennsylvania'),
    'Kansas': ('USA', 'Topeka, Kansas'),
    'The Allman Brothers Band': ('USA', 'Jacksonville, Florida'),
    'Interpol': ('USA', 'New York, New York'),
    'Serge Gainsbourg & Jane Birkin': ('France', 'Paris'),
    'Modest Mouse': ('USA', 'Issaquah, Washington'),
    'David Bowie': ('UK', 'London'),
    'Steve Earle': ('USA', 'Fort Monroe, Virginia'),
    'Kurt Vile': ('USA', 'Philadelphia, Pennsylvania'),
    'Spoon': ('USA', 'Austin, Texas'),
    'Fleetwood Mac': ('UK', 'London'),
    'R.E.M.': ('USA', 'Athens, Georgia'),
    'Widespread Panic': ('USA', 'Athens, Georgia'),
    'J. Geils Band': ('USA', 'Worcester, Massachusetts'),
    'Jethro Tull': ('UK', 'Blackpool'),
    'The Stone Roses': ('UK', 'Manchester'),
    'Grouplove': ('USA', 'Los Angeles, California'),
    'The Wombats': ('UK', 'Liverpool'),
    'Wilco': ('USA', 'Chicago, Illinois'),
    'Pavement': ('USA', 'Stockton, California'),
    'Sonic Youth': ('USA', 'New York, New York'),
    'The Orwells': ('USA', 'Elmhurst, Illinois'),
    'Sleater-Kinney': ('USA', 'Olympia, Washington'),
    'Pixies': ('USA', 'Boston, Massachusetts'),
    'Los Campesinos!': ('UK', 'Cardiff, Wales'),
    'John Prine': ('USA', 'Maywood, Illinois'),
    'Led Zeppelin': ('UK', 'London'),
    'Mott the Hoople': ('UK', 'Hereford'),
    'Roy Buchanan': ('USA', 'Ozark, Arkansas'),
    'Tears for Fears': ('UK', 'Bath, Somerset'),
    'Beck': ('USA', 'Los Angeles, California'),
    'Dinosaur Jr.': ('USA', 'Amherst, Massachusetts'),
    'J Mascis': ('USA', 'Amherst, Massachusetts'),
    'Japandroids': ('Canada', 'Vancouver, British Columbia'),
    'Father John Misty': ('USA', 'Rockville, Maryland'),
    'Van Morrison': ('UK', 'Belfast, Northern Ireland'),
    'Band of Horses': ('USA', 'Seattle, Washington'),
    'Brand New': ('USA', 'Long Island, New York'),
    'TV on the Radio': ('USA', 'Brooklyn, New York'),
    'Arc Angels': ('USA', 'Austin, Texas'),
    'Yes': ('UK', 'London'),
    'Good Night Lights': ('USA', 'USA'),
    'The Church': ('Australia', 'Sydney'),
    'Treepeople': ('USA', 'Boise, Idaho'),
    'Joe Strummer and the Mescaleros': ('UK', 'London'),
    'Van Halen': ('USA', 'Pasadena, California'),
    'Haim': ('USA', 'Los Angeles, California'),
    'The Smiths': ('UK', 'Manchester'),
    'Nêhiyawak': ('Canada', 'Edmonton, Alberta'),
    'Myles Cane': ('Canada', 'Canada'),
    'Television': ('USA', 'New York, New York'),
    'Devo': ('USA', 'Akron, Ohio'),
    'The Clash': ('UK', 'London'),
    'Leon Bridges': ('USA', 'Fort Worth, Texas'),
    'Billie Eilish': ('USA', 'Los Angeles, California'),
    'Harry Styles': ('UK', 'Redditch, Worcestershire'),
    'William Orbit': ('UK', 'London'),
    'The Connells': ('USA', 'Raleigh, North Carolina'),
    'The Stranglers': ('UK', 'Guildford, Surrey'),
    'Dry Cleaning': ('UK', 'London'),
    'The War on Drugs': ('USA', 'Philadelphia, Pennsylvania'),
    'My Morning Jacket': ('USA', 'Louisville, Kentucky'),
    'The Charlatans UK': ('UK', 'West Midlands'),
    'Gomez': ('UK', 'Southport'),
    'IDLES': ('UK', 'Bristol'),
    'Depeche Mode': ('UK', 'Basildon, Essex'),
    'Kraftwerk': ('Germany', 'Düsseldorf'),
    'The Police': ('UK', 'London'),
    'Bob Seger': ('USA', 'Detroit, Michigan'),
    'Gil Scott-Heron': ('USA', 'Chicago, Illinois'),
    'Echo & the Bunnymen': ('UK', 'Liverpool'),
    'Twenty One Pilots': ('USA', 'Columbus, Ohio'),
    'Metric': ('Canada', 'Toronto, Ontario'),
    'The Doors': ('USA', 'Los Angeles, California'),
    'The Strokes': ('USA', 'New York, New York'),
    'Ron Gallo': ('USA', 'Philadelphia, Pennsylvania'),
    'Foo Fighters': ('USA', 'Seattle, Washington'),
    'Sky Ferreira': ('USA', 'Los Angeles, California'),
    'Bloc Party': ('UK', 'London'),
    'Cut Copy': ('Australia', 'Melbourne'),
    'The Cure': ('UK', 'Crawley, West Sussex'),
    'Supertramp': ('UK', 'London'),
    'St. Paul and the Broken Bones': ('USA', 'Birmingham, Alabama'),
    'Sharon Jones & The Dap-Kings': ('USA', 'Brooklyn, New York'),
    'INXS': ('Australia', 'Sydney'),
    'Jackson Browne': ('USA', 'Heidelberg, Germany'),
    'Todd Rundgren': ('USA', 'Philadelphia, Pennsylvania'),
    'Pink Floyd': ('UK', 'London'),
    'Nilüfer Yanya': ('UK', 'London'),
    'PJ Harvey': ('UK', 'Bridport, Dorset'),
    'Yeah Yeah Yeahs': ('USA', 'New York, New York'),
    'Fall Out Boy': ('USA', 'Wilmette, Illinois'),
    'Blink-182': ('USA', 'Poway, California'),
    'Taking Back Sunday': ('USA', 'Long Island, New York'),
    'Killing Joke': ('UK', 'Notting Hill, London'),
    'Tubeway Army': ('UK', 'London'),
    'Nine Inch Nails': ('USA', 'Cleveland, Ohio'),
    'Neil Young & Crazy Horse': ('Canada', 'Toronto, Ontario'),
    'Johnny Marr and the Healers': ('UK', 'Manchester'),
    'Morrissey': ('UK', 'Manchester'),
    'Woods': ('USA', 'Brooklyn, New York'),
    'King Gizzard & the Lizard Wizard': ('Australia', 'Melbourne'),
    'Neil Young': ('Canada', 'Toronto, Ontario'),
    'Pet Fox': ('USA', 'Brooklyn, New York'),
    'Momma': ('USA', 'Los Angeles, California'),
    'Shame': ('UK', 'London'),
    'Maximo Park': ('UK', 'Newcastle upon Tyne'),
    'The Futureheads': ('UK', 'Sunderland'),
    'Phantom Planet': ('USA', 'Los Angeles, California'),
    'MGMT': ('USA', 'Middletown, Connecticut'),
    'The Beatles': ('UK', 'Liverpool'),
    'Nirvana': ('USA', 'Aberdeen, Washington'),
    'Manchester Orchestra': ('USA', 'Atlanta, Georgia'),
}

# add origin data to each album
for album in albums:
    artist = album['artist']
    if artist in artist_origins:
        nation, city = artist_origins[artist]
        album['nation_of_origin'] = nation
        album['city_of_origin'] = city
    else:
        album['nation_of_origin'] = 'Unknown'
        album['city_of_origin'] = 'Unknown'
        print(f"Warning: No origin data for '{artist}'")

# save updated data
with open('vcl_albums.json', 'w', encoding='utf-8') as f:
    json.dump(albums, f, indent=2)

with open('vcl_albums.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['meeting_number', 'meeting_date', 'presenter', 'album_position',
                  'artist', 'album_title', 'release_year', 'label', 'genre',
                  'nation_of_origin', 'city_of_origin']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(albums)

print(f"updated {len(albums)} albums with origin data")

# stats
real_albums = [a for a in albums if a['artist'] != 'Various']
nation_counts = Counter(a['nation_of_origin'] for a in real_albums)

print("\nalbums by nation:")
for nation, count in nation_counts.most_common():
    print(f"  {nation}: {count}")

# count unique artists
unique_artists = len(set(a['artist'] for a in real_albums))
print(f"\nunique artists: {unique_artists}")
