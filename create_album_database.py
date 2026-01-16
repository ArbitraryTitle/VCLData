#!/usr/bin/env python3
import json
import csv

# manually curated album data with metadata
# format: (meeting_num, date, presenter, position, artist, album, year, label, genre)

albums_data = [
    # Meeting 1
    (1, '1/22/2015', 'Chris', 'headliner', 'King Crimson', 'In the Court of the Crimson King', 1969, 'Island', 'Progressive Rock'),

    # Meeting 2
    (2, '2/26/2015', 'Joe', 'headliner', 'Mountain', 'Nantucket Sleighride', 1971, 'Windfall', 'Hard Rock'),

    # Meeting 3
    (3, '3/27/2015', 'John', 'warm_up_1', 'Sebadoh', 'Sebadoh III', 1991, 'Homestead', 'Indie Rock'),
    (3, '3/27/2015', 'John', 'warm_up_2', 'Yo La Tengo', 'I Can Hear the Heart Beating as One', 1997, 'Matador', 'Indie Rock'),
    (3, '3/27/2015', 'John', 'headliner', 'Ben Lee', 'Grandpaw Would', 1995, 'Modular', 'Alternative Rock'),

    # Meeting 4
    (4, '4/23/2015', 'Chris', 'headliner', 'The Knife', 'Silent Shout', 2006, 'Rabid', 'Electronic'),

    # Meeting 5
    (5, '7/29/2015', 'Joe', 'warm_up_1', 'Jefferson Airplane', 'Surrealistic Pillow', 1967, 'RCA Victor', 'Psychedelic Rock'),
    (5, '7/29/2015', 'Joe', 'warm_up_2', 'Talking Heads', 'Talking Heads: 77', 1977, 'Sire', 'New Wave'),

    # Meeting 6
    (6, '11/5/2015', 'John', 'headliner', 'The Afghan Whigs', 'Black Love', 1996, 'Elektra', 'Alternative Rock'),

    # Meeting 7
    (7, '12/17/2015', 'Chris', 'headliner', 'The Stooges', 'Raw Power', 1973, 'Columbia', 'Punk Rock'),

    # Meeting 8
    (8, '1/26/2016', 'Joe', 'warm_up_1', 'James Brown', 'Say It Loud', 1969, 'King', 'Funk'),
    (8, '1/26/2016', 'Joe', 'warm_up_2', 'Various Artists', 'David Bowie Tribute', 2016, 'Various', 'Rock'),

    # Meeting 9
    (9, '3/25/2016', 'Lucas', 'warm_up_1', 'Paul Simon', 'Graceland', 1986, 'Warner Bros.', 'World Music'),
    (9, '3/25/2016', 'Lucas', 'warm_up_2', 'Arcade Fire', 'Funeral', 2004, 'Merge', 'Indie Rock'),
    (9, '3/25/2016', 'Lucas', 'headliner', 'Vampire Weekend', 'Vampire Weekend', 2008, 'XL', 'Indie Rock'),

    # Meeting 10
    (10, '5/26/2016', 'John', 'warm_up_1', 'The Replacements', 'Pleased to Meet Me', 1987, 'Sire', 'Alternative Rock'),
    (10, '5/26/2016', 'John', 'warm_up_2', 'The Jam', 'Setting Sons', 1979, 'Polydor', 'Punk Rock'),
    (10, '5/26/2016', 'John', 'headliner', 'Big Star', '#1 Record', 1972, 'Ardent', 'Power Pop'),

    # Meeting 11
    (11, '8/10/2016', 'Chris', 'warm_up_1', 'Joy Division', 'Unknown Pleasures', 1979, 'Factory', 'Post-Punk'),
    (11, '8/10/2016', 'Chris', 'warm_up_2', 'Genesis', 'Selling England by the Pound', 1973, 'Charisma', 'Progressive Rock'),
    (11, '8/10/2016', 'Chris', 'headliner', 'Radiohead', 'A Moon Shaped Pool', 2016, 'XL', 'Alternative Rock'),

    # Meeting 12
    (12, '9/29/2016', 'Joe', 'warm_up_1', 'Adrian Belew', 'Young Lions', 1990, 'Atlantic', 'Art Rock'),
    (12, '9/29/2016', 'Joe', 'warm_up_2', 'Robin Trower', 'Bridge of Sighs', 1974, 'Chrysalis', 'Blues Rock'),
    (12, '9/29/2016', 'Joe', 'headliner', 'Santana', 'Moonflower', 1977, 'Columbia', 'Latin Rock'),

    # Meeting 13
    (13, '12/8/2016', 'Lucas', 'warm_up_1', 'Frightened Rabbit', 'Midnight Organ Fight', 2008, 'Fat Cat', 'Indie Rock'),
    (13, '12/8/2016', 'Lucas', 'warm_up_2', 'Leonard Cohen', 'Various Positions', 1984, 'Columbia', 'Folk'),
    (13, '12/8/2016', 'Lucas', 'headliner', 'Bob Dylan', 'Blood on the Tracks', 1975, 'Columbia', 'Folk Rock'),

    # Meeting 14
    (14, '1/26/2017', 'John', 'warm_up_1', 'Galaxie 500', 'On Fire', 1989, '4AD', 'Dream Pop'),
    (14, '1/26/2017', 'John', 'warm_up_2', 'Morphine', 'Cure for Pain', 1993, 'Rykodisc', 'Alternative Rock'),
    (14, '1/26/2017', 'John', 'headliner', 'Built to Spill', 'Perfect from Now On', 1997, 'Warner Bros.', 'Indie Rock'),

    # Meeting 15
    (15, '3/9/2017', 'Chris', 'warm_up_1', 'MC5', 'Kick Out the Jams', 1969, 'Elektra', 'Punk Rock'),
    (15, '3/9/2017', 'Chris', 'warm_up_2', 'Mastodon', 'Crack the Skye', 2009, 'Reprise', 'Progressive Metal'),
    (15, '3/9/2017', 'Chris', 'headliner', 'Black Sabbath', 'Vol. 4', 1972, 'Vertigo', 'Heavy Metal'),

    # Meeting 16
    (16, '5/4/2017', 'Joe', 'warm_up_1', 'Live', 'Mental Jewelry', 1991, 'Radioactive', 'Alternative Rock'),
    (16, '5/4/2017', 'Joe', 'warm_up_2', 'Kansas', 'Leftoverture', 1976, 'Kirshner', 'Progressive Rock'),
    (16, '5/4/2017', 'Joe', 'headliner', 'The Allman Brothers Band', 'At Fillmore East', 1971, 'Capricorn', 'Southern Rock'),

    # Meeting 17
    (17, '8/10/2017', 'Lucas', 'warm_up_1', 'Interpol', 'Turn On the Bright Lights', 2002, 'Matador', 'Post-Punk Revival'),
    (17, '8/10/2017', 'Lucas', 'warm_up_2', 'Serge Gainsbourg & Jane Birkin', 'Jane Birkin/Serge Gainsbourg', 1969, 'Fontana', 'Chanson'),
    (17, '8/10/2017', 'Lucas', 'headliner', 'Modest Mouse', 'The Moon & Antarctica', 2000, 'Epic', 'Indie Rock'),

    # Meeting 18
    (18, '9/14/2017', 'John', 'warm_up_1', 'David Bowie', 'Pin Ups', 1973, 'RCA', 'Glam Rock'),
    (18, '9/14/2017', 'John', 'warm_up_2', 'Steve Earle', 'Townes', 2009, 'New West', 'Country'),
    (18, '9/14/2017', 'John', 'headliner', 'Kurt Vile', "Believe I'm Going Down", 2015, 'Matador', 'Indie Rock'),

    # Meeting 19
    (19, '10/26/2017', 'Chris', 'warm_up_1', 'Spoon', 'Ga Ga Ga Ga Ga', 2007, 'Merge', 'Indie Rock'),
    (19, '10/26/2017', 'Chris', 'warm_up_2', 'Fleetwood Mac', 'Rumours', 1977, 'Warner Bros.', 'Rock'),
    (19, '10/26/2017', 'Chris', 'headliner', 'R.E.M.', 'Murmur', 1983, 'I.R.S.', 'Alternative Rock'),

    # Meeting 20
    (20, '1/25/2018', 'Joe', 'warm_up_1', 'Widespread Panic', 'VCL Mix Edition', 2018, 'Various', 'Jam Band'),
    (20, '1/25/2018', 'Joe', 'warm_up_2', 'J. Geils Band', 'The Morning After', 1971, 'Atlantic', 'Rock'),
    (20, '1/25/2018', 'Joe', 'headliner', 'Jethro Tull', 'Thick as a Brick', 1972, 'Chrysalis', 'Progressive Rock'),

    # Meeting 21
    (21, '3/8/2018', 'Eric', 'warm_up_1', 'The Stone Roses', 'The Stone Roses', 1989, 'Silvertone', 'Madchester'),
    (21, '3/8/2018', 'Eric', 'warm_up_2', 'Grouplove', 'Never Trust a Happy Song', 2011, 'Canvasback', 'Indie Rock'),
    (21, '3/8/2018', 'Eric', 'headliner', 'The Wombats', 'Beautiful People Will Ruin Your Life', 2018, 'Kobalt', 'Indie Rock'),

    # Meeting 22
    (22, '5/10/2018', 'John', 'warm_up_1', 'Wilco', 'Yankee Hotel Foxtrot', 2002, 'Nonesuch', 'Alternative Country'),
    (22, '5/10/2018', 'John', 'warm_up_2', 'Pavement', 'Slanted and Enchanted', 1992, 'Matador', 'Indie Rock'),
    (22, '5/10/2018', 'John', 'headliner', 'Sonic Youth', 'Daydream Nation', 1988, 'Enigma', 'Alternative Rock'),

    # Meeting 23
    (23, '8/9/2018', 'Adam', 'warm_up_1', 'The Orwells', 'Disgraceland', 2017, 'Canvasback', 'Garage Rock'),
    (23, '8/9/2018', 'Adam', 'warm_up_2', 'Sleater-Kinney', 'Dig Me Out', 1997, 'Kill Rock Stars', 'Riot Grrrl'),
    (23, '8/9/2018', 'Adam', 'headliner', 'Pixies', 'Doolittle', 1989, '4AD', 'Alternative Rock'),

    # Meeting 24
    (24, '11/1/2018', 'Lucas', 'warm_up_1', 'Los Campesinos!', 'No Blues', 2013, 'Wichita', 'Indie Rock'),
    (24, '11/1/2018', 'Lucas', 'warm_up_2', 'John Prine', 'Bruised Orange', 1978, 'Asylum', 'Country Folk'),

    # Meeting 25
    (25, '1/24/2019', 'Chris', 'warm_up_1', 'Led Zeppelin', 'Led Zeppelin', 1969, 'Atlantic', 'Hard Rock'),
    (25, '1/24/2019', 'Chris', 'headliner', 'Led Zeppelin', 'Led Zeppelin II', 1969, 'Atlantic', 'Hard Rock'),

    # Meeting 26
    (26, '3/7/2019', 'Joe', 'warm_up_1', 'Mott the Hoople', 'All the Young Dudes', 1972, 'Columbia', 'Glam Rock'),
    (26, '3/7/2019', 'Joe', 'warm_up_2', 'Roy Buchanan', "That's What I Am Here For", 1973, 'Polydor', 'Blues Rock'),

    # Meeting 27
    (27, '5/2/2019', 'Eric', 'warm_up_1', 'Tears for Fears', 'Elemental', 1993, 'Mercury', 'Pop Rock'),
    (27, '5/2/2019', 'Eric', 'headliner', 'Beck', 'Guero', 2005, 'Interscope', 'Alternative Rock'),

    # Meeting 28
    (28, '9/5/2019', 'John', 'warm_up_1', 'Dinosaur Jr.', "You're Living All Over Me", 1987, 'SST', 'Alternative Rock'),
    (28, '9/5/2019', 'John', 'warm_up_2', 'J Mascis', 'Elastic Days', 2018, 'Sub Pop', 'Indie Rock'),

    # Meeting 29
    (29, '10/7/2019', 'Adam', 'warm_up_1', 'Japandroids', 'Celebration Rock', 2012, 'Polyvinyl', 'Indie Rock'),
    (29, '10/7/2019', 'Adam', 'headliner', 'Arcade Fire', 'Funeral', 2004, 'Merge', 'Indie Rock'),

    # Meeting 30
    (30, '1/23/2020', 'Lucas', 'warm_up_1', 'Father John Misty', 'Fear Fun', 2012, 'Sub Pop', 'Folk Rock'),
    (30, '1/23/2020', 'Lucas', 'headliner', 'Van Morrison', 'Astral Weeks', 1968, 'Warner Bros.', 'Folk Rock'),

    # Meeting 31
    (31, '6/11/2020', 'Chris', 'warm_up_1', 'Band of Horses', 'Everything All the Time', 2006, 'Sub Pop', 'Indie Rock'),
    (31, '6/11/2020', 'Chris', 'warm_up_2', 'Brand New', 'The Devil and God Are Raging Inside Me', 2006, 'Interscope', 'Emo'),
    (31, '6/11/2020', 'Chris', 'headliner', 'TV on the Radio', 'Return to Cookie Mountain', 2006, 'Interscope', 'Art Rock'),

    # Meeting 32
    (32, '8/6/2020', 'Joe', 'warm_up_1', 'Arc Angels', 'Arc Angels', 1992, 'Geffen', 'Blues Rock'),
    (32, '8/6/2020', 'Joe', 'warm_up_2', 'Yes', 'Close to the Edge', 1972, 'Atlantic', 'Progressive Rock'),
    (32, '8/6/2020', 'Joe', 'headliner', 'Good Night Lights', 'Biggest Fears', 2019, 'Independent', 'Indie Rock'),

    # Meeting 33
    (33, '9/24/2020', 'John', 'warm_up_1', 'The Church', 'Starfish', 1988, 'Arista', 'Alternative Rock'),
    (33, '9/24/2020', 'John', 'warm_up_2', 'Treepeople', 'Something Vicious for Tomorrow / Time Whore', 1994, 'C/Z', 'Grunge'),
    (33, '9/24/2020', 'John', 'headliner', 'Joe Strummer and the Mescaleros', 'Streetcore', 2003, 'Hellcat', 'Punk Rock'),

    # Meeting 34
    (34, '11/19/2020', 'Eric', 'warm_up_1', 'Van Halen', '1984', 1984, 'Warner Bros.', 'Hard Rock'),
    (34, '11/19/2020', 'Eric', 'warm_up_2', 'Haim', 'Days Are Gone', 2013, 'Polydor', 'Pop Rock'),
    (34, '11/19/2020', 'Eric', 'headliner', 'The Smiths', 'Louder Than Bombs', 1987, 'Sire', 'Alternative Rock'),

    # Meeting 35
    (35, '3/11/2021', 'Adam', 'warm_up_1', 'Nêhiyawak', 'nipiy', 2020, 'Independent', 'Indigenous Hip Hop'),
    (35, '3/11/2021', 'Adam', 'warm_up_2', 'Myles Cane', 'Coup de Grace', 2020, 'Independent', 'Indie Rock'),
    (35, '3/11/2021', 'Adam', 'headliner', 'The Afghan Whigs', 'Up in It', 1990, 'Sub Pop', 'Alternative Rock'),

    # Meeting 36
    (36, '5/13/2021', 'Chris', 'warm_up_1', 'Television', 'Marquee Moon', 1977, 'Elektra', 'Punk Rock'),
    (36, '5/13/2021', 'Chris', 'warm_up_2', 'Devo', 'Q: Are We Not Men? A: We Are Devo!', 1978, 'Warner Bros.', 'New Wave'),
    (36, '5/13/2021', 'Chris', 'headliner', 'The Clash', 'London Calling', 1979, 'CBS', 'Punk Rock'),

    # Meeting 37
    (37, '6/10/2021', 'Joe', 'warm_up_1', 'Leon Bridges', 'Coming Home', 2015, 'Columbia', 'Soul'),
    (37, '6/10/2021', 'Joe', 'warm_up_2', 'Billie Eilish', 'When We All Fall Asleep, Where Do We Go?', 2019, 'Interscope', 'Pop'),
    (37, '6/10/2021', 'Joe', 'headliner', 'Harry Styles', 'Fine Line', 2019, 'Columbia', 'Pop Rock'),

    # Meeting 38
    (38, '9/7/2021', 'Eric', 'warm_up_1', 'William Orbit', 'My Oracle Lives Uptown', 2019, 'Guerilla', 'Electronic'),
    (38, '9/7/2021', 'Eric', 'warm_up_2', 'The Connells', "Steadman's Wake", 2001, 'Black Park', 'Jangle Pop'),
    (38, '9/7/2021', 'Eric', 'headliner', 'The Stranglers', 'Dark Matters', 2021, 'Coursegood', 'Post-Punk'),

    # Meeting 39
    (39, '11/23/2021', 'John', 'warm_up_1', 'Dry Cleaning', 'New Long Leg', 2021, '4AD', 'Post-Punk'),
    (39, '11/23/2021', 'John', 'warm_up_2', 'The War on Drugs', "I Don't Live Here Anymore", 2021, 'Atlantic', 'Indie Rock'),
    (39, '11/23/2021', 'John', 'headliner', 'My Morning Jacket', 'My Morning Jacket', 2021, 'ATO', 'Southern Rock'),

    # Meeting 40
    (40, '04/14/2022', 'Adam', 'warm_up_1', 'The Charlatans UK', 'Between 10th and 11th', 1992, 'Situation Two', 'Madchester'),
    (40, '04/14/2022', 'Adam', 'warm_up_2', 'Gomez', 'Bring It On', 1998, 'Hut', 'Alternative Rock'),
    (40, '04/14/2022', 'Adam', 'headliner', 'IDLES', 'Crawler', 2021, 'Partisan', 'Post-Punk'),

    # Meeting 41
    (41, '6/9/2022', 'Chris', 'warm_up_1', 'Depeche Mode', 'Speak & Spell', 1981, 'Mute', 'Synthpop'),
    (41, '6/9/2022', 'Chris', 'warm_up_2', 'Kraftwerk', 'Computer World', 1981, 'Kling Klang', 'Electronic'),
    (41, '6/9/2022', 'Chris', 'headliner', 'The Police', 'Ghost in the Machine', 1981, 'A&M', 'New Wave'),

    # Meeting 42
    (42, '7/14/2022', 'Joe', 'warm_up_1', 'Bob Seger', 'Live Bullet', 1976, 'Capitol', 'Rock'),
    (42, '7/14/2022', 'Joe', 'warm_up_2', 'Gil Scott-Heron', 'Pieces of a Man', 1971, 'Flying Dutchman', 'Jazz Poetry'),
    (42, '7/14/2022', 'Joe', 'headliner', 'Tears for Fears', 'The Tipping Point', 2022, 'Concord', 'Pop Rock'),

    # Meeting 43
    (43, '8/11/2022', 'Eric', 'warm_up_1', 'Echo & the Bunnymen', 'Evergreen', 1997, 'London', 'Alternative Rock'),
    (43, '8/11/2022', 'Eric', 'warm_up_2', 'Twenty One Pilots', 'Vessel', 2013, 'Fueled by Ramen', 'Alternative Rock'),
    (43, '8/11/2022', 'Eric', 'headliner', 'Metric', 'Art of Doubt', 2018, 'Crystal Math', 'Indie Rock'),

    # Meeting 44
    (44, '9/15/2022', 'John', 'warm_up_1', 'The Doors', 'The Doors', 1967, 'Elektra', 'Psychedelic Rock'),
    (44, '9/15/2022', 'John', 'headliner', 'The Strokes', 'Is This It', 2001, 'RCA', 'Garage Rock Revival'),

    # Meeting 45
    (45, '11/17/2022', 'Adam', 'warm_up_1', 'Ron Gallo', 'Heavy Meta', 2017, 'New West', 'Garage Rock'),
    (45, '11/17/2022', 'Adam', 'headliner', 'Foo Fighters', 'The Colour and the Shape', 1997, 'Roswell', 'Alternative Rock'),

    # Meeting 46
    (46, '1/12/2023', 'Lucas', 'warm_up_1', 'Sky Ferreira', 'Night Time, My Time', 2013, 'Capitol', 'Indie Pop'),
    (46, '1/12/2023', 'Lucas', 'headliner', 'Bloc Party', 'Silent Alarm', 2005, 'Wichita', 'Post-Punk Revival'),

    # Meeting 47
    (47, '3/9/2023', 'Chris', 'warm_up_1', 'Cut Copy', 'In Ghost Colours', 2008, 'Modular', 'Electronic'),
    (47, '3/9/2023', 'Chris', 'headliner', 'The Cure', 'Kiss Me, Kiss Me, Kiss Me', 1987, 'Fiction', 'Alternative Rock'),

    # Meeting 48
    (48, '4/20/2023', 'Joe', 'warm_up_1', 'Supertramp', 'Crime of the Century', 1974, 'A&M', 'Progressive Rock'),
    (48, '4/20/2023', 'Joe', 'warm_up_2', 'St. Paul and the Broken Bones', 'The Alien Coast', 2020, 'ATO', 'Soul'),
    (48, '4/20/2023', 'Joe', 'headliner', 'Sharon Jones & The Dap-Kings', '100 Days, 100 Nights', 2007, 'Daptone', 'Soul'),

    # Meeting 49
    (49, '6/8/2023', 'Eric', 'warm_up_1', 'The Police', 'Zenyatta Mondatta', 1980, 'A&M', 'New Wave'),
    (49, '6/8/2023', 'Eric', 'warm_up_2', 'INXS', 'The Swing', 1984, 'Mercury', 'New Wave'),
    (49, '6/8/2023', 'Eric', 'headliner', 'Jackson Browne', 'Late for the Sky', 1974, 'Asylum', 'Folk Rock'),

    # Meeting 50
    (50, '7/13/2023', 'John', 'warm_up_1', 'Todd Rundgren', 'A Wizard, a True Star', 1973, 'Bearsville', 'Art Rock'),
    (50, '7/13/2023', 'John', 'warm_up_2', 'Pink Floyd', 'Animals', 1977, 'Harvest', 'Progressive Rock'),
    (50, '7/13/2023', 'John', 'headliner', 'Yo La Tengo', 'This Stupid World', 2023, 'Matador', 'Indie Rock'),

    # Meeting 51
    (51, '9/21/2023', 'Adam', 'warm_up_1', 'Nilüfer Yanya', 'Painless', 2022, 'ATO', 'Alternative Rock'),
    (51, '9/21/2023', 'Adam', 'warm_up_2', 'PJ Harvey', 'Stories from the City, Stories from the Sea', 2000, 'Island', 'Alternative Rock'),
    (51, '9/21/2023', 'Adam', 'headliner', 'Yeah Yeah Yeahs', 'Fever to Tell', 2003, 'Interscope', 'Indie Rock'),

    # Meeting 52
    (52, '10/19/2023', 'Lucas', 'warm_up_1', 'Fall Out Boy', 'From Under the Cork Tree', 2005, 'Island', 'Pop Punk'),
    (52, '10/19/2023', 'Lucas', 'warm_up_2', 'Blink-182', 'Blink-182', 2003, 'Geffen', 'Pop Punk'),
    (52, '10/19/2023', 'Lucas', 'headliner', 'Taking Back Sunday', 'Tell All Your Friends', 2002, 'Victory', 'Emo'),

    # Meeting 53
    (53, '11/9/2023', 'Chris', 'warm_up_1', 'Killing Joke', 'Killing Joke', 1980, 'E.G.', 'Post-Punk'),
    (53, '11/9/2023', 'Chris', 'warm_up_2', 'Tubeway Army', 'Tubeway Army', 1978, 'Beggars Banquet', 'Post-Punk'),
    (53, '11/9/2023', 'Chris', 'headliner', 'Nine Inch Nails', 'The Fragile', 1999, 'Nothing', 'Industrial Rock'),

    # Meeting 54
    (54, '1/10/2024', 'Joe', 'headliner', 'Neil Young & Crazy Horse', 'Live at the Fillmore 1970', 2006, 'Reprise', 'Rock'),

    # Meeting 55
    (55, '3/14/2024', 'Eric', 'warm_up_1', 'Johnny Marr and the Healers', 'Boomslang', 2003, 'Artistdirect', 'Alternative Rock'),
    (55, '3/14/2024', 'Eric', 'warm_up_2', 'Morrissey', 'Viva Hate', 1988, 'HMV', 'Alternative Rock'),
    (55, '3/14/2024', 'Eric', 'headliner', 'The Smiths', 'Hatful of Hollow', 1984, 'Rough Trade', 'Alternative Rock'),

    # Meeting 56
    (56, '4/11/2024', 'John', 'warm_up_1', 'Woods', 'Perennial', 2023, 'Woodsist', 'Indie Rock'),
    (56, '4/11/2024', 'John', 'warm_up_2', 'King Gizzard & the Lizard Wizard', 'Ice, Death, Planets, Lungs, Mushrooms and Lava', 2022, 'KGLW', 'Psychedelic Rock'),
    (56, '4/11/2024', 'John', 'headliner', 'Neil Young', 'Chrome Dreams', 2007, 'Reprise', 'Folk Rock'),

    # Meeting 57
    (57, '5/9/2024', 'Adam', 'warm_up_1', 'Pet Fox', 'A Face in Your Life', 2024, 'Carpark', 'Indie Rock'),
    (57, '5/9/2024', 'Adam', 'warm_up_2', 'Momma', 'Household Name', 2022, 'Polyvinyl', 'Alternative Rock'),
    (57, '5/9/2024', 'Adam', 'headliner', 'Shame', 'Songs of Praise', 2018, 'Dead Oceans', 'Post-Punk'),

    # Meeting 58
    (58, '9/12/2024', 'Lucas', 'warm_up_1', 'Bloc Party', 'A Weekend in the City', 2007, 'Wichita', 'Post-Punk Revival'),
    (58, '9/12/2024', 'Lucas', 'warm_up_2', 'Maximo Park', 'A Certain Trigger', 2005, 'Warp', 'Post-Punk Revival'),
    (58, '9/12/2024', 'Lucas', 'headliner', 'The Futureheads', 'The Futureheads', 2004, '679', 'Post-Punk Revival'),

    # Meeting 60 (note: no 59 in data)
    (60, '10/10/2024', 'Chris', 'warm_up_1', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),
    (60, '10/10/2024', 'Chris', 'warm_up_2', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),
    (60, '10/10/2024', 'Chris', 'headliner', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),

    # Meeting 61
    (61, '11/21/2024', 'Joe', 'warm_up_1', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),
    (61, '11/21/2024', 'Joe', 'warm_up_2', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),
    (61, '11/21/2024', 'Joe', 'headliner', 'Various', 'To Be Announced', 2024, 'TBA', 'TBA'),

    # Meeting 62
    (62, '1/9/2025', 'John', 'warm_up_1', 'Various', 'To Be Announced', 2025, 'TBA', 'TBA'),
    (62, '1/9/2025', 'John', 'warm_up_2', 'Various', 'To Be Announced', 2025, 'TBA', 'TBA'),
    (62, '1/9/2025', 'John', 'headliner', 'Various', 'To Be Announced', 2025, 'TBA', 'TBA'),

    # Meeting 63
    (63, '3/13/2025', 'Adam', 'warm_up_1', 'Phantom Planet', 'Phantom Planet', 2004, 'Epic', 'Indie Rock'),
    (63, '3/13/2025', 'Adam', 'warm_up_2', 'MGMT', 'Loss of Life', 2024, 'Mom + Pop', 'Psychedelic Pop'),
    (63, '3/13/2025', 'Adam', 'headliner', 'The Beatles', 'Magical Mystery Tour', 1967, 'Capitol', 'Psychedelic Rock'),

    # Meeting 64
    (64, '5/22/2025', 'Lucas', 'warm_up_1', 'Nirvana', 'Incesticide', 1992, 'DGC', 'Grunge'),
    (64, '5/22/2025', 'Lucas', 'warm_up_2', 'Manchester Orchestra', 'A Black Mile to the Surface', 2017, 'Loma Vista', 'Alternative Rock'),
    (64, '5/22/2025', 'Lucas', 'headliner', 'Radiohead', 'In Rainbows', 2007, 'XL', 'Alternative Rock'),
]

# convert to list of dicts
albums = []
for entry in albums_data:
    albums.append({
        'meeting_number': entry[0],
        'meeting_date': entry[1],
        'presenter': entry[2],
        'album_position': entry[3],
        'artist': entry[4],
        'album_title': entry[5],
        'release_year': entry[6],
        'label': entry[7],
        'genre': entry[8]
    })

# filter out TBA entries for stats
real_albums = [a for a in albums if a['artist'] != 'Various']

# save as csv
with open('vcl_albums.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['meeting_number', 'meeting_date', 'presenter', 'album_position', 'artist', 'album_title', 'release_year', 'label', 'genre']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(albums)

# save as json
with open('vcl_albums.json', 'w', encoding='utf-8') as f:
    json.dump(albums, f, indent=2)

print(f"created album database with {len(real_albums)} albums")
print(f"\ntotal entries (including TBA): {len(albums)}")
print(f"confirmed albums: {len(real_albums)}")

# stats
from collections import Counter

genre_counts = Counter(a['genre'] for a in real_albums)
decade_counts = Counter(str(a['release_year'])[:3] + '0s' for a in real_albums if a['release_year'] != 'TBA')
presenter_counts = Counter(a['presenter'] for a in real_albums)

print("\ntop 10 genres:")
for genre, count in genre_counts.most_common(10):
    print(f"  {genre}: {count}")

print("\nalbums by decade:")
for decade in sorted(decade_counts.keys()):
    print(f"  {decade}: {decade_counts[decade]}")

print("\nalbums per presenter:")
for presenter in sorted(presenter_counts.keys()):
    print(f"  {presenter}: {presenter_counts[presenter]}")

print("\nfiles created:")
print("  - vcl_albums.csv")
print("  - vcl_albums.json")
