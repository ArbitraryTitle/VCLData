#!/usr/bin/env python3
import json
import csv

# load current album data
with open('Music/Data/vcl_albums.json', 'r') as f:
    albums = json.load(f)

# micro-niche genre mappings
# format: (artist, album) -> niche_genre
micro_genres = {
    ('King Crimson', 'In the Court of the Crimson King'): 'Symphonic Prog',
    ('Mountain', 'Nantucket Sleighride'): 'Proto-Metal',
    ('Sebadoh', 'Sebadoh III'): 'Lo-Fi Indie Rock',
    ('Yo La Tengo', 'I Can Hear the Heart Beating as One'): 'Indie Pop / Noise Pop',
    ('Ben Lee', 'Grandpaw Would'): 'Twee Pop',
    ('The Knife', 'Silent Shout'): 'Synthpop / Minimal Wave',
    ('Jefferson Airplane', 'Surrealistic Pillow'): 'Acid Rock',
    ('Talking Heads', 'Talking Heads: 77'): 'Art Punk / No Wave',
    ('The Afghan Whigs', 'Black Love'): 'Grunge / Alternative R&B',
    ('The Stooges', 'Raw Power'): 'Proto-Punk',
    ('James Brown', 'Say It Loud'): 'Funk / Soul Jazz',
    ('Various Artists', 'David Bowie Tribute'): 'Tribute Album',
    ('Paul Simon', 'Graceland'): 'Worldbeat / Sophisti-Pop',
    ('Arcade Fire', 'Funeral'): 'Baroque Pop',
    ('Vampire Weekend', 'Vampire Weekend'): 'Afro-Pop Influenced Indie',
    ('The Replacements', 'Pleased to Meet Me'): 'Cowpunk / Power Pop',
    ('The Jam', 'Setting Sons'): 'Mod Revival / Power Pop',
    ('Big Star', '#1 Record'): 'Jangle Pop / Power Pop',
    ('Joy Division', 'Unknown Pleasures'): 'Post-Punk / Coldwave',
    ('Genesis', 'Selling England by the Pound'): 'Symphonic Prog',
    ('Radiohead', 'A Moon Shaped Pool'): 'Art Rock / Chamber Pop',
    ('Adrian Belew', 'Young Lions'): 'Progressive Pop / Art Rock',
    ('Robin Trower', 'Bridge of Sighs'): 'Blues Rock / Psychedelic Blues',
    ('Santana', 'Moonflower'): 'Latin Rock / Jazz Fusion',
    ('Frightened Rabbit', 'Midnight Organ Fight'): 'Scottish Indie Rock',
    ('Leonard Cohen', 'Various Positions'): 'Chamber Folk',
    ('Bob Dylan', 'Blood on the Tracks'): 'Singer-Songwriter / Heartland Rock',
    ('Galaxie 500', 'On Fire'): 'Slowcore / Dream Pop',
    ('Morphine', 'Cure for Pain'): 'Low Rock / Noir Jazz',
    ('Built to Spill', 'Perfect from Now On'): 'Indie Rock / Midwest Emo Influenced',
    ('MC5', 'Kick Out the Jams'): 'Proto-Punk / Garage Rock',
    ('Mastodon', 'Crack the Skye'): 'Progressive Sludge Metal',
    ('Black Sabbath', 'Vol. 4'): 'Heavy Psych / Doom Metal',
    ('Live', 'Mental Jewelry'): 'Grunge / Post-Grunge',
    ('Kansas', 'Leftoverture'): 'Arena Rock / Symphonic Prog',
    ('The Allman Brothers Band', 'At Fillmore East'): 'Southern Rock / Blues Rock',
    ('Interpol', 'Turn On the Bright Lights'): 'Post-Punk Revival / Art Punk',
    ('Serge Gainsbourg & Jane Birkin', 'Jane Birkin/Serge Gainsbourg'): 'Yé-Yé / Baroque Pop',
    ('Modest Mouse', 'The Moon & Antarctica'): 'Indie Rock / Art Rock',
    ('David Bowie', 'Pin Ups'): 'Glam Rock / Art Rock',
    ('Steve Earle', 'Townes'): 'Outlaw Country / Americana',
    ('Kurt Vile', "Believe I'm Going Down"): 'Slacker Rock / Neo-Psychedelia',
    ('Spoon', 'Ga Ga Ga Ga Ga'): 'Indie Rock / Post-Punk Revival',
    ('Fleetwood Mac', 'Rumours'): 'Soft Rock / West Coast Pop',
    ('R.E.M.', 'Murmur'): 'Jangle Pop / College Rock',
    ('Widespread Panic', 'VCL Mix Edition'): 'Southern Rock / Jam Band',
    ('J. Geils Band', 'The Morning After'): 'Blue-Eyed Soul / R&B Rock',
    ('Jethro Tull', 'Thick as a Brick'): 'Progressive Rock / Folk Prog',
    ('The Stone Roses', 'The Stone Roses'): 'Madchester / Baggy',
    ('Grouplove', 'Never Trust a Happy Song'): 'Indie Pop / Dance-Punk',
    ('The Wombats', 'Beautiful People Will Ruin Your Life'): 'Indie Pop / Dance-Punk',
    ('Wilco', 'Yankee Hotel Foxtrot'): 'Art Rock / Experimental Rock',
    ('Pavement', 'Slanted and Enchanted'): 'Lo-Fi Indie / Slacker Rock',
    ('Sonic Youth', 'Daydream Nation'): 'Noise Rock / No Wave',
    ('The Orwells', 'Disgraceland'): 'Garage Punk Revival',
    ('Sleater-Kinney', 'Dig Me Out'): 'Riot Grrrl / Post-Hardcore',
    ('Pixies', 'Doolittle'): 'Noise Pop / Surf Punk',
    ('Los Campesinos!', 'No Blues'): 'Twee Pop / Emo',
    ('John Prine', 'Bruised Orange'): 'Outlaw Country / Country Folk',
    ('Led Zeppelin', 'Led Zeppelin'): 'Blues Rock / Heavy Psych',
    ('Led Zeppelin', 'Led Zeppelin II'): 'Hard Rock / Heavy Blues',
    ('Mott the Hoople', 'All the Young Dudes'): 'Glam Rock / Proto-Punk',
    ('Roy Buchanan', "That's What I Am Here For"): 'Blues Rock / Telecaster Blues',
    ('Tears for Fears', 'Elemental'): 'Sophisti-Pop / Art Pop',
    ('Beck', 'Guero'): 'Alternative Hip Hop / Neo-Psychedelia',
    ('Dinosaur Jr.', "You're Living All Over Me"): 'Noise Rock / Hardcore Punk',
    ('J Mascis', 'Elastic Days'): 'Singer-Songwriter / Neo-Psychedelia',
    ('Japandroids', 'Celebration Rock'): 'Noise Pop / Post-Hardcore',
    ('Father John Misty', 'Fear Fun'): 'Baroque Pop / Chamber Folk',
    ('Van Morrison', 'Astral Weeks'): 'Celtic Soul / Chamber Jazz',
    ('Band of Horses', 'Everything All the Time'): 'Heartland Rock / Indie Folk',
    ('Brand New', 'The Devil and God Are Raging Inside Me'): 'Emo / Post-Hardcore',
    ('TV on the Radio', 'Return to Cookie Mountain'): 'Art Punk / Post-Punk Revival',
    ('Arc Angels', 'Arc Angels'): 'Texas Blues / Southern Rock',
    ('Yes', 'Close to the Edge'): 'Symphonic Prog / Art Rock',
    ('Good Night Lights', 'Biggest Fears'): 'Indie Rock',
    ('The Church', 'Starfish'): 'Jangle Pop / Dream Pop',
    ('Treepeople', 'Something Vicious for Tomorrow / Time Whore'): 'Post-Hardcore / Emo',
    ('Joe Strummer and the Mescaleros', 'Streetcore'): 'Worldbeat / Folk Punk',
    ('Van Halen', '1984'): 'Hard Rock / Arena Rock',
    ('Haim', 'Days Are Gone'): 'Soft Rock Revival / Indie Pop',
    ('The Smiths', 'Louder Than Bombs'): 'Jangle Pop / Post-Punk',
    ('Nêhiyawak', 'nipiy'): 'Indigenous Hip Hop / Experimental',
    ('Myles Cane', 'Coup de Grace'): 'Indie Rock',
    ('The Afghan Whigs', 'Up in It'): 'Grunge / Cowpunk',
    ('Television', 'Marquee Moon'): 'Art Punk / Proto-Post-Punk',
    ('Devo', 'Q: Are We Not Men? A: We Are Devo!'): 'Art Punk / Synth Punk',
    ('The Clash', 'London Calling'): 'Punk Rock / New Wave',
    ('Leon Bridges', 'Coming Home'): 'Neo-Soul / Retro Soul',
    ('Billie Eilish', 'When We All Fall Asleep, Where Do We Go?'): 'Alt-Pop / Bedroom Pop',
    ('Harry Styles', 'Fine Line'): 'Soft Rock / Yacht Rock Revival',
    ('William Orbit', 'My Oracle Lives Uptown'): 'Ambient Pop / Electronica',
    ('The Connells', "Steadman's Wake"): 'Jangle Pop / College Rock',
    ('The Stranglers', 'Dark Matters'): 'Post-Punk / Pub Rock',
    ('Dry Cleaning', 'New Long Leg'): 'Post-Punk / Spoken Word Rock',
    ('The War on Drugs', "I Don't Live Here Anymore"): 'Heartland Rock / Neo-Psychedelia',
    ('My Morning Jacket', 'My Morning Jacket'): 'Southern Rock / Psychedelic Folk',
    ('The Charlatans UK', 'Between 10th and 11th'): 'Madchester / Baggy',
    ('Gomez', 'Bring It On'): 'Blues Rock / Trip Hop',
    ('IDLES', 'Crawler'): 'Post-Punk / Art Punk',
    ('Depeche Mode', 'Speak & Spell'): 'Synthpop / New Romantic',
    ('Kraftwerk', 'Computer World'): 'Krautrock / Electro',
    ('The Police', 'Ghost in the Machine'): 'New Wave / Post-Punk',
    ('Bob Seger', 'Live Bullet'): 'Heartland Rock / Arena Rock',
    ('Gil Scott-Heron', 'Pieces of a Man'): 'Jazz Poetry / Proto-Hip Hop',
    ('Tears for Fears', 'The Tipping Point'): 'Sophisti-Pop / Art Pop',
    ('Echo & the Bunnymen', 'Evergreen'): 'Neo-Psychedelia / Post-Punk',
    ('Twenty One Pilots', 'Vessel'): 'Electropop / Emo Rap',
    ('Metric', 'Art of Doubt'): 'Indie Rock / Synth Rock',
    ('The Doors', 'The Doors'): 'Acid Rock / Psychedelic Blues',
    ('The Strokes', 'Is This It'): 'Garage Rock Revival / Post-Punk Revival',
    ('Ron Gallo', 'Heavy Meta'): 'Garage Rock / Proto-Punk Revival',
    ('Foo Fighters', 'The Colour and the Shape'): 'Post-Grunge / Power Pop',
    ('Sky Ferreira', 'Night Time, My Time'): 'Synth-Pop / Dream Pop',
    ('Bloc Party', 'Silent Alarm'): 'Post-Punk Revival / Dance-Punk',
    ('Cut Copy', 'In Ghost Colours'): 'Synth-Pop / Nu-Disco',
    ('The Cure', 'Kiss Me, Kiss Me, Kiss Me'): 'Gothic Rock / Jangle Pop',
    ('Supertramp', 'Crime of the Century'): 'Art Rock / Progressive Pop',
    ('St. Paul and the Broken Bones', 'The Alien Coast'): 'Southern Soul / Gospel Soul',
    ('Sharon Jones & The Dap-Kings', '100 Days, 100 Nights'): 'Deep Soul / Funk',
    ('The Police', 'Zenyatta Mondatta'): 'New Wave / Reggae Rock',
    ('INXS', 'The Swing'): 'New Wave / Funk Rock',
    ('Jackson Browne', 'Late for the Sky'): 'Singer-Songwriter / Soft Rock',
    ('Todd Rundgren', 'A Wizard, a True Star'): 'Art Pop / Progressive Pop',
    ('Pink Floyd', 'Animals'): 'Progressive Rock / Art Rock',
    ('Yo La Tengo', 'This Stupid World'): 'Indie Rock / Noise Pop',
    ('Nilüfer Yanya', 'Painless'): 'Art Pop / Neo-Psychedelia',
    ('PJ Harvey', 'Stories from the City, Stories from the Sea'): 'Art Rock / Alternative Rock',
    ('Yeah Yeah Yeahs', 'Fever to Tell'): 'Dance-Punk / Art Punk',
    ('Fall Out Boy', 'From Under the Cork Tree'): 'Pop Punk / Emo Pop',
    ('Blink-182', 'Blink-182'): 'Pop Punk / Skate Punk',
    ('Taking Back Sunday', 'Tell All Your Friends'): 'Emo / Post-Hardcore',
    ('Killing Joke', 'Killing Joke'): 'Post-Punk / Industrial Rock',
    ('Tubeway Army', 'Tubeway Army'): 'Synth-Punk / Proto-Synth-Pop',
    ('Nine Inch Nails', 'The Fragile'): 'Industrial Rock / Art Rock',
    ('Neil Young & Crazy Horse', 'Live at the Fillmore 1970'): 'Jam Band / Folk Rock',
    ('Johnny Marr and the Healers', 'Boomslang'): 'Indie Rock / Jangle Pop',
    ('Morrissey', 'Viva Hate'): 'Jangle Pop / Art Pop',
    ('The Smiths', 'Hatful of Hollow'): 'Jangle Pop / Post-Punk',
    ('Woods', 'Perennial'): 'Freak Folk / Lo-Fi Indie',
    ('King Gizzard & the Lizard Wizard', 'Ice, Death, Planets, Lungs, Mushrooms and Lava'): 'Psychedelic Rock / Krautrock',
    ('Neil Young', 'Chrome Dreams'): 'Folk Rock / Country Rock',
    ('Pet Fox', 'A Face in Your Life'): 'Indie Rock / Jangle Pop',
    ('Momma', 'Household Name'): 'Grunge Revival / Shoegaze',
    ('Shame', 'Songs of Praise'): 'Post-Punk / Art Punk',
    ('Bloc Party', 'A Weekend in the City'): 'Post-Punk Revival / Indie Rock',
    ('Maximo Park', 'A Certain Trigger'): 'Post-Punk Revival / Art Punk',
    ('The Futureheads', 'The Futureheads'): 'Post-Punk Revival / Art Punk',
    ('Phantom Planet', 'Phantom Planet'): 'Power Pop / Indie Rock',
    ('MGMT', 'Loss of Life'): 'Psychedelic Pop / Neo-Psychedelia',
    ('The Beatles', 'Magical Mystery Tour'): 'Psychedelic Pop / Baroque Pop',
    ('Nirvana', 'Incesticide'): 'Grunge / Punk Rock',
    ('Manchester Orchestra', 'A Black Mile to the Surface'): 'Indie Rock / Emo',
    ('Radiohead', 'In Rainbows'): 'Art Rock / Electronic',
    ('Various', 'To Be Announced'): 'TBA',
}

# add micro genre to each album
for album in albums:
    key = (album['artist'], album['album_title'])
    if key in micro_genres:
        album['micro_genre'] = micro_genres[key]
    else:
        # fallback to regular genre
        album['micro_genre'] = album['genre']
        print(f"Warning: No micro genre for {album['artist']} - {album['album_title']}")

# save updated data
with open('Music/Data/vcl_albums.json', 'w', encoding='utf-8') as f:
    json.dump(albums, f, indent=2)

with open('Music/Data/vcl_albums.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['meeting_number', 'meeting_date', 'presenter', 'album_position',
                  'artist', 'album_title', 'release_year', 'label', 'genre', 'micro_genre',
                  'nation_of_origin', 'city_of_origin']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(albums)

print(f"updated {len(albums)} albums with micro-niche genres")

# count unique micro genres
from collections import Counter
real_albums = [a for a in albums if a['artist'] != 'Various']
micro_genre_counts = Counter(a['micro_genre'] for a in real_albums)

print(f"\ntotal unique micro genres: {len(micro_genre_counts)}")
print("\nmost common micro genres:")
for mg, count in micro_genre_counts.most_common(10):
    print(f"  {mg}: {count}")

print("\nsome choice micro genres:")
samples = [
    'Slowcore / Dream Pop',
    'Low Rock / Noir Jazz',
    'Yé-Yé / Baroque Pop',
    'Celtic Soul / Chamber Jazz',
    'Proto-Hip Hop',
    'Baggy',
    'Telecaster Blues',
    'Cowpunk',
    'Spoken Word Rock'
]
for s in samples:
    if s in micro_genre_counts:
        print(f"  {s}")
