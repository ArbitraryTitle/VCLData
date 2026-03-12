# Proposed Album Data Schema

Based on the PowerPoint data, here's what I can extract and what I'd propose to add:

## Columns Available from PowerPoint:
1. **meeting_number** - sequential meeting number (1-64)
2. **meeting_date** - date of VCL meeting
3. **presenter** - who presented the album(s)
4. **album_position** - warm-up 1, warm-up 2, or headliner (most meetings have 2-3 albums)
5. **artist** - band/artist name
6. **album_title** - album name

## Columns I Can Add by Research:
7. **release_year** - year album was released
8. **release_date** - full release date if available
9. **label** - record label
10. **genre** - primary genre (rock, punk, alternative, etc.)
11. **subgenre** - more specific genre tags
12. **producer** - producer(s)

## Calculated/Analysis Columns:
13. **decade** - derived from release_year (1960s, 1970s, etc.)
14. **era** - broader groupings (60s-70s, 80s-90s, 2000s+)

## Issues I See in the Data:
- Some "Selections" entries have multiple albums separated by commas
- Format varies: sometimes "Artist Album", sometimes just "Album", sometimes "Artist - Album"
- Some entries are tributes or special formats (e.g., "David Bowie tribute")
- Need to parse ~150-200 individual albums from the 64 meetings

## Proposed Approach:
1. Extract all album entries from the history tables
2. Parse artist/album from the freeform text
3. Research release years, labels, genres for each
4. Create normalized spreadsheet

Want me to proceed with this schema? Any columns you'd want to add/remove?
