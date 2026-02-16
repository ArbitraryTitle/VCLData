#!/usr/bin/env python3
import json
import re
import csv

# load tables data
with open('tables_raw.json', 'r') as f:
    tables = json.load(f)

# extract all album entries
albums_raw = []

for table in tables:
    if 'rows' in table:
        rows = table['rows']
        # skip header row
        for row in rows[1:]:
            if len(row) >= 5 and row[0] and row[0] != '#' and row[4]:  # has meeting #, date, mc, cocktail, selections
                meeting_num = row[0]
                date = row[1]
                presenter = row[2]
                selections = row[4]

                if selections and selections != '0':
                    albums_raw.append({
                        'meeting_number': meeting_num,
                        'date': date,
                        'presenter': presenter,
                        'selections_raw': selections
                    })

print(f"extracted {len(albums_raw)} meeting records with albums")

# now parse individual albums from selections
# format is usually "Artist Album Title, Artist2 Album2, Artist3 Album3"
# sometimes "Artist - Album" or just "Album"

def parse_albums(selections_text):
    """Parse album text into individual album entries"""
    albums = []

    # split by comma or semicolon
    parts = re.split(r'[,;]', selections_text)

    for part in parts:
        part = part.strip()
        if not part or part == '0':
            continue

        # try to parse artist - album format
        if ' – ' in part or ' - ' in part:
            # split on dash
            split_char = ' – ' if ' – ' in part else ' - '
            parts_split = part.split(split_char, 1)
            artist = parts_split[0].strip()
            album = parts_split[1].strip() if len(parts_split) > 1 else ''
            albums.append({'artist': artist, 'album': album})
        else:
            # try to identify where artist ends and album begins
            # usually format is "Artist Name Album Title"
            # heuristic: look for common patterns
            words = part.split()

            # some known patterns
            if len(words) >= 2:
                # try to find where album title likely starts
                # this is imperfect but we'll refine manually
                artist = ' '.join(words[:2]) if len(words) > 2 else words[0]
                album = ' '.join(words[2:]) if len(words) > 2 else words[1] if len(words) > 1 else ''
                albums.append({'artist': artist, 'album': album, 'raw': part})
            else:
                albums.append({'artist': '', 'album': part, 'raw': part})

    return albums

# parse all albums
all_albums = []
position_counter = {}  # track position per meeting

for entry in albums_raw:
    meeting_num = entry['meeting_number']

    # reset position counter for each meeting
    if meeting_num not in position_counter:
        position_counter[meeting_num] = 0

    parsed = parse_albums(entry['selections_raw'])

    for album_data in parsed:
        position_counter[meeting_num] += 1
        position = position_counter[meeting_num]

        # determine album position
        if position == 1:
            album_position = 'warm_up_1'
        elif position == 2:
            album_position = 'warm_up_2'
        elif position == 3:
            album_position = 'headliner'
        else:
            album_position = f'additional_{position}'

        all_albums.append({
            'meeting_number': entry['meeting_number'],
            'meeting_date': entry['date'],
            'presenter': entry['presenter'],
            'album_position': album_position,
            'artist': album_data.get('artist', ''),
            'album_title': album_data.get('album', ''),
            'raw_text': album_data.get('raw', entry['selections_raw'])
        })

# save preliminary data
with open('Music/Data/albums_preliminary.json', 'w') as f:
    json.dump(all_albums, f, indent=2)

with open('albums_preliminary.csv', 'w', newline='', encoding='utf-8') as f:
    if all_albums:
        fieldnames = ['meeting_number', 'meeting_date', 'presenter', 'album_position', 'artist', 'album_title', 'raw_text']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_albums)

print(f"\nparsed {len(all_albums)} individual albums")
print("\nfirst 10 albums:")
for i, album in enumerate(all_albums[:10], 1):
    print(f"{i}. {album['artist']} - {album['album_title']} (meeting {album['meeting_number']}, {album['album_position']})")

print("\nsaved preliminary data to albums_preliminary.json and albums_preliminary.csv")
print("\nnow i need to manually clean up the artist/album parsing and add metadata...")
