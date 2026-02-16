#!/usr/bin/env python3
import json
import csv

# load current album data
with open('vcl_albums.json', 'r') as f:
    albums = json.load(f)

# full release dates for all albums
# format: (artist, album) -> 'YYYY-MM-DD'
release_dates = {
    ('King Crimson', 'In the Court of the Crimson King'): '1969-10-10',
    ('Mountain', 'Nantucket Sleighride'): '1971-01-01',
    ('Sebadoh', 'Sebadoh III'): '1991-09-01',
    ('Yo La Tengo', 'I Can Hear the Heart Beating as One'): '1997-04-22',
    ('Ben Lee', 'Grandpaw Would'): '1995-08-28',
    ('The Knife', 'Silent Shout'): '2006-02-17',
    ('Jefferson Airplane', 'Surrealistic Pillow'): '1967-02-01',
    ('Talking Heads', 'Talking Heads: 77'): '1977-09-16',
    ('The Afghan Whigs', 'Black Love'): '1996-03-12',
    ('The Stooges', 'Raw Power'): '1973-02-07',
    ('James Brown', 'Say It Loud'): '1969-01-01',
    ('Various Artists', 'David Bowie Tribute'): '2016-01-01',
    ('Paul Simon', 'Graceland'): '1986-08-25',
    ('Arcade Fire', 'Funeral'): '2004-09-14',
    ('Vampire Weekend', 'Vampire Weekend'): '2008-01-29',
    ('The Replacements', 'Pleased to Meet Me'): '1987-07-01',
    ('The Jam', 'Setting Sons'): '1979-11-16',
    ('Big Star', '#1 Record'): '1972-04-24',
    ('Joy Division', 'Unknown Pleasures'): '1979-06-15',
    ('Genesis', 'Selling England by the Pound'): '1973-10-12',
    ('Radiohead', 'A Moon Shaped Pool'): '2016-05-08',
    ('Adrian Belew', 'Young Lions'): '1990-11-13',
    ('Robin Trower', 'Bridge of Sighs'): '1974-04-01',
    ('Santana', 'Moonflower'): '1977-10-01',
    ('Frightened Rabbit', 'Midnight Organ Fight'): '2008-04-14',
    ('Leonard Cohen', 'Various Positions'): '1984-12-11',
    ('Bob Dylan', 'Blood on the Tracks'): '1975-01-20',
    ('Galaxie 500', 'On Fire'): '1989-10-01',
    ('Morphine', 'Cure for Pain'): '1993-09-14',
    ('Built to Spill', 'Perfect from Now On'): '1997-02-11',
    ('MC5', 'Kick Out the Jams'): '1969-02-01',
    ('Mastodon', 'Crack the Skye'): '2009-03-24',
    ('Black Sabbath', 'Vol. 4'): '1972-09-25',
    ('Live', 'Mental Jewelry'): '1991-12-31',
    ('Kansas', 'Leftoverture'): '1976-10-01',
    ('The Allman Brothers Band', 'At Fillmore East'): '1971-07-01',
    ('Interpol', 'Turn On the Bright Lights'): '2002-08-20',
    ('Serge Gainsbourg & Jane Birkin', 'Jane Birkin/Serge Gainsbourg'): '1969-07-01',
    ('Modest Mouse', 'The Moon & Antarctica'): '2000-06-13',
    ('David Bowie', 'Pin Ups'): '1973-10-19',
    ('Steve Earle', 'Townes'): '2009-05-12',
    ('Kurt Vile', "Believe I'm Going Down"): '2015-09-25',
    ('Spoon', 'Ga Ga Ga Ga Ga'): '2007-07-10',
    ('Fleetwood Mac', 'Rumours'): '1977-02-04',
    ('R.E.M.', 'Murmur'): '1983-04-12',
    ('Widespread Panic', 'VCL Mix Edition'): '2018-01-01',
    ('J. Geils Band', 'The Morning After'): '1971-10-01',
    ('Jethro Tull', 'Thick as a Brick'): '1972-03-03',
    ('The Stone Roses', 'The Stone Roses'): '1989-05-02',
    ('Grouplove', 'Never Trust a Happy Song'): '2011-09-13',
    ('The Wombats', 'Beautiful People Will Ruin Your Life'): '2018-02-09',
    ('Wilco', 'Yankee Hotel Foxtrot'): '2002-04-23',
    ('Pavement', 'Slanted and Enchanted'): '1992-04-20',
    ('Sonic Youth', 'Daydream Nation'): '1988-10-18',
    ('The Orwells', 'Disgraceland'): '2017-06-09',
    ('Sleater-Kinney', 'Dig Me Out'): '1997-04-08',
    ('Pixies', 'Doolittle'): '1989-04-18',
    ('Los Campesinos!', 'No Blues'): '2013-10-29',
    ('John Prine', 'Bruised Orange'): '1978-09-01',
    ('Led Zeppelin', 'Led Zeppelin'): '1969-01-12',
    ('Led Zeppelin', 'Led Zeppelin II'): '1969-10-22',
    ('Mott the Hoople', 'All the Young Dudes'): '1972-09-08',
    ('Roy Buchanan', "That's What I Am Here For"): '1973-01-01',
    ('Tears for Fears', 'Elemental'): '1993-06-22',
    ('Beck', 'Guero'): '2005-03-29',
    ('Dinosaur Jr.', "You're Living All Over Me"): '1987-12-14',
    ('J Mascis', 'Elastic Days'): '2018-11-09',
    ('Japandroids', 'Celebration Rock'): '2012-06-05',
    ('Father John Misty', 'Fear Fun'): '2012-04-30',
    ('Van Morrison', 'Astral Weeks'): '1968-11-01',
    ('Band of Horses', 'Everything All the Time'): '2006-03-21',
    ('Brand New', 'The Devil and God Are Raging Inside Me'): '2006-11-21',
    ('TV on the Radio', 'Return to Cookie Mountain'): '2006-07-06',
    ('Arc Angels', 'Arc Angels'): '1992-10-13',
    ('Yes', 'Close to the Edge'): '1972-09-13',
    ('Good Night Lights', 'Biggest Fears'): '2019-01-01',
    ('The Church', 'Starfish'): '1988-02-08',
    ('Treepeople', 'Something Vicious for Tomorrow / Time Whore'): '1994-01-01',
    ('Joe Strummer and the Mescaleros', 'Streetcore'): '2003-10-21',
    ('Van Halen', '1984'): '1984-01-09',
    ('Haim', 'Days Are Gone'): '2013-09-27',
    ('The Smiths', 'Louder Than Bombs'): '1987-03-30',
    ('Nêhiyawak', 'nipiy'): '2020-09-25',
    ('Myles Cane', 'Coup de Grace'): '2020-01-01',
    ('The Afghan Whigs', 'Up in It'): '1990-10-23',
    ('Television', 'Marquee Moon'): '1977-02-08',
    ('Devo', 'Q: Are We Not Men? A: We Are Devo!'): '1978-08-28',
    ('The Clash', 'London Calling'): '1979-12-14',
    ('Leon Bridges', 'Coming Home'): '2015-06-23',
    ('Billie Eilish', 'When We All Fall Asleep, Where Do We Go?'): '2019-03-29',
    ('Harry Styles', 'Fine Line'): '2019-12-13',
    ('William Orbit', 'My Oracle Lives Uptown'): '2019-09-27',
    ('The Connells', "Steadman's Wake"): '2001-09-11',
    ('The Stranglers', 'Dark Matters'): '2021-09-10',
    ('Dry Cleaning', 'New Long Leg'): '2021-04-02',
    ('The War on Drugs', "I Don't Live Here Anymore"): '2021-10-29',
    ('My Morning Jacket', 'My Morning Jacket'): '2021-10-22',
    ('The Charlatans UK', 'Between 10th and 11th'): '1992-02-17',
    ('Gomez', 'Bring It On'): '1998-04-13',
    ('IDLES', 'Crawler'): '2021-11-12',
    ('Depeche Mode', 'Speak & Spell'): '1981-10-05',
    ('Kraftwerk', 'Computer World'): '1981-05-10',
    ('The Police', 'Ghost in the Machine'): '1981-10-02',
    ('Bob Seger', 'Live Bullet'): '1976-04-01',
    ('Gil Scott-Heron', 'Pieces of a Man'): '1971-01-01',
    ('Tears for Fears', 'The Tipping Point'): '2022-02-25',
    ('Echo & the Bunnymen', 'Evergreen'): '1997-07-08',
    ('Twenty One Pilots', 'Vessel'): '2013-01-08',
    ('Metric', 'Art of Doubt'): '2018-09-21',
    ('The Doors', 'The Doors'): '1967-01-04',
    ('The Strokes', 'Is This It'): '2001-07-30',
    ('Ron Gallo', 'Heavy Meta'): '2017-02-03',
    ('Foo Fighters', 'The Colour and the Shape'): '1997-05-20',
    ('Sky Ferreira', 'Night Time, My Time'): '2013-10-29',
    ('Bloc Party', 'Silent Alarm'): '2005-02-02',
    ('Cut Copy', 'In Ghost Colours'): '2008-03-07',
    ('The Cure', 'Kiss Me, Kiss Me, Kiss Me'): '1987-05-26',
    ('Supertramp', 'Crime of the Century'): '1974-09-13',
    ('St. Paul and the Broken Bones', 'The Alien Coast'): '2020-01-24',
    ('Sharon Jones & The Dap-Kings', '100 Days, 100 Nights'): '2007-10-02',
    ('The Police', 'Zenyatta Mondatta'): '1980-10-03',
    ('INXS', 'The Swing'): '1984-04-02',
    ('Jackson Browne', 'Late for the Sky'): '1974-09-13',
    ('Todd Rundgren', 'A Wizard, a True Star'): '1973-03-02',
    ('Pink Floyd', 'Animals'): '1977-01-23',
    ('Yo La Tengo', 'This Stupid World'): '2023-02-10',
    ('Nilüfer Yanya', 'Painless'): '2022-03-04',
    ('PJ Harvey', 'Stories from the City, Stories from the Sea'): '2000-10-23',
    ('Yeah Yeah Yeahs', 'Fever to Tell'): '2003-04-29',
    ('Fall Out Boy', 'From Under the Cork Tree'): '2005-05-03',
    ('Blink-182', 'Blink-182'): '2003-11-18',
    ('Taking Back Sunday', 'Tell All Your Friends'): '2002-03-26',
    ('Killing Joke', 'Killing Joke'): '1980-10-01',
    ('Tubeway Army', 'Tubeway Army'): '1978-11-01',
    ('Nine Inch Nails', 'The Fragile'): '1999-09-21',
    ('Neil Young & Crazy Horse', 'Live at the Fillmore 1970'): '2006-11-07',
    ('Johnny Marr and the Healers', 'Boomslang'): '2003-02-03',
    ('Morrissey', 'Viva Hate'): '1988-03-14',
    ('The Smiths', 'Hatful of Hollow'): '1984-11-12',
    ('Woods', 'Perennial'): '2023-01-27',
    ('King Gizzard & the Lizard Wizard', 'Ice, Death, Planets, Lungs, Mushrooms and Lava'): '2022-10-07',
    ('Neil Young', 'Chrome Dreams'): '2007-10-23',
    ('Pet Fox', 'A Face in Your Life'): '2024-01-26',
    ('Momma', 'Household Name'): '2022-07-01',
    ('Shame', 'Songs of Praise'): '2018-01-12',
    ('Bloc Party', 'A Weekend in the City'): '2007-02-05',
    ('Maximo Park', 'A Certain Trigger'): '2005-05-16',
    ('The Futureheads', 'The Futureheads'): '2004-09-13',
    ('Phantom Planet', 'Phantom Planet'): '2004-01-06',
    ('MGMT', 'Loss of Life'): '2024-02-23',
    ('The Beatles', 'Magical Mystery Tour'): '1967-11-27',
    ('Nirvana', 'Incesticide'): '1992-12-14',
    ('Manchester Orchestra', 'A Black Mile to the Surface'): '2017-07-21',
    ('Radiohead', 'In Rainbows'): '2007-10-10',
    ('Various', 'To Be Announced'): None,
}

# add release date to each album
for album in albums:
    key = (album['artist'], album['album_title'])
    if key in release_dates:
        album['release_date'] = release_dates[key]
    else:
        album['release_date'] = None
        print(f"Warning: No release date for {album['artist']} - {album['album_title']}")

# save updated data
with open('vcl_albums.json', 'w', encoding='utf-8') as f:
    json.dump(albums, f, indent=2)

with open('vcl_albums.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['meeting_number', 'meeting_date', 'presenter', 'album_position',
                  'artist', 'album_title', 'release_year', 'release_date', 'label', 'genre', 'micro_genre',
                  'nation_of_origin', 'city_of_origin']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(albums)

print(f"updated {len(albums)} albums with full release dates")

# stats
real_albums = [a for a in albums if a.get('release_date')]
print(f"\nalbums with dates: {len(real_albums)}")

# find some interesting dates
import datetime

albums_with_parsed_dates = []
for a in real_albums:
    try:
        date_obj = datetime.datetime.strptime(a['release_date'], '%Y-%m-%d')
        albums_with_parsed_dates.append((a, date_obj))
    except:
        pass

# oldest and newest
albums_with_parsed_dates.sort(key=lambda x: x[1])
print("\noldest albums:")
for a, d in albums_with_parsed_dates[:5]:
    print(f"  {d.strftime('%B %d, %Y')}: {a['artist']} - {a['album_title']}")

print("\nnewest albums:")
for a, d in albums_with_parsed_dates[-5:]:
    print(f"  {d.strftime('%B %d, %Y')}: {a['artist']} - {a['album_title']}")
