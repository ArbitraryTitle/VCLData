# VCL Cocktail Dashboard - Tableau Build Guide

## data setup

1. download `cocktail_history_tableau.csv` from this repo
2. open tableau desktop
3. connect to data: **connect > to a file > text file**
4. select `cocktail_history_tableau.csv`
5. in the data source tab, verify:
   - `latitude` and `longitude` are recognized as numbers (decimal)
   - `year_invented` is recognized as a number
   - `date` is recognized as a date
   - all others as strings

---

## visualization 1: origin map

**goal:** world map showing where cocktails originated with bubble size = count

**steps:**
1. create new sheet, name it "origin map"
2. double-click `latitude` (should create a map)
3. drag `longitude` to columns
4. drag `cocktail` to detail (this creates one mark per cocktail)
5. drag `city_of_origin` to detail
6. right-click on the map marks > **aggregate measures** (should be checked)
7. change mark type from automatic to **circle**
8. drag `city_of_origin` to **size** (bigger bubbles = more cocktails)
9. drag `city_of_origin` to **color**
10. drag `cocktail` to **label** and/or **tooltip**
11. adjust:
    - map > map layers > style = normal
    - size slider to make bubbles visible
    - tooltip to show: city, country, cocktail names

**alternative:** use tableau's built-in geocoding:
- drag `city_of_origin` to detail
- drag `country_of_origin` to detail
- tableau should auto-create lat/lon
- if it doesn't recognize cities, use custom lat/lon we provided

---

## visualization 2: cocktails by host (stacked bar)

**goal:** stacked bar chart showing each host's cocktails, colored by country or liquor

**steps for country view:**
1. create new sheet, name it "by host - country"
2. drag `host` to columns
3. drag `cocktail` to rows (this will create a bar per cocktail)
4. click the **sort descending** button on host axis
5. right-click on `cocktail` in rows > **measure > count**
6. drag `country_of_origin` to **color**
7. change mark type to **bar**
8. make bars **stacked**: analysis > stack marks > on
9. adjust colors in the color legend if desired
10. add labels: drag `country_of_origin` to label

**steps for liquor view:**
1. duplicate the sheet (right-click > duplicate)
2. rename to "by host - liquor"
3. replace `country_of_origin` with `primary_liquor` in color
4. update tooltip/labels accordingly

**to create toggle buttons:**
- in dashboard, create parameter for "view type"
- use parameter actions to switch between sheets
- or just put both sheets in dashboard with tabs

---

## visualization 3: timeline

**goal:** scatter plot of cocktails over time, colored by presenter

**steps:**
1. create new sheet, name it "timeline"
2. drag `year_invented` to columns
3. drag `cocktail` to rows (or create a calculated field for vertical spacing)
4. drag `host` to **color**
5. change mark type to **circle**
6. drag `cocktail` to **label**
7. adjust:
   - make circles bigger (size slider)
   - rotate labels if they overlap: label > alignment > horizontal
   - filter out any null years if needed
8. add reference lines for key eras:
   - analytics pane > drag **reference line** to x-axis
   - add lines at 1900, 1920, 1933, 2000
   - label them: "1900", "prohibition", "repeal", "craft era"

**vertical spacing trick:**
if cocktails overlap, create calculated field:
- name: `row number`
- formula: `INDEX()`
- drag to rows instead of cocktail
- drag `cocktail` to label and tooltip

---

## visualization 4: overview stats

**goal:** summary charts showing liquor distribution and era breakdown

**liquor bar chart:**
1. create new sheet, name it "liquor breakdown"
2. drag `primary_liquor` to rows
3. drag `cocktail` to columns
4. right-click `cocktail` > measure > count
5. change mark type to **bar**
6. sort descending
7. drag `primary_liquor` to color (optional)
8. add data labels: drag `CNT(cocktail)` to label

**era bar chart:**
1. create new sheet, name it "era breakdown"
2. drag `era` to columns
3. drag `cocktail` to rows
4. right-click `cocktail` > measure > count
5. change mark type to **bar**
6. sort by era chronologically (may need to create calculated field for sorting)
7. drag `era` to color with gradient
8. add data labels

---

## dashboard assembly

**steps:**
1. create new dashboard
2. set size: **automatic** or **desktop (1400x900)**
3. drag sheets onto dashboard in this layout:

```
+----------------------------------+
|     HEADER (text box)            |
+----------------------------------+
| stat | stat | stat | stat        |  <- use text boxes or BANs
+----------------------------------+
|  liquor chart  |  era chart      |
+----------------------------------+
|          origin map              |
+----------------------------------+
|      by host (stacked bar)       |
+----------------------------------+
|          timeline                |
+----------------------------------+
```

4. add header text box:
   - "VCL Cocktail Dashboard"
   - "visualizing 10 years of cocktail presentations (2015-2025)"

5. add stat boxes (use text objects):
   - 63 total cocktails
   - 20 cities of origin
   - 245 years of history
   - 6 presenters

6. add filters (optional):
   - drag `host` to dashboard > show filter
   - drag `primary_liquor` to dashboard > show filter
   - drag `era` to dashboard > show filter
   - set filters to apply to all sheets

7. add interactivity:
   - select each sheet > use as filter
   - clicking on map bubbles filters other charts
   - clicking on host bars filters timeline

---

## color schemes

**hosts:**
- chris: blue (#1f77b4)
- joe: orange (#ff7f0e)
- john: green (#2ca02c)
- lucas: red (#d62728)
- adam: purple (#9467bd)
- eric: brown (#8c564b)

**liquors:**
- whiskey: saddle brown
- gin: sky blue
- vodka: lavender
- rum: sandy brown
- tequila: gold
- brandy: indian red
- other: gray

to set custom colors:
1. click color legend
2. edit colors
3. enter hex codes above

---

## tips

- **performance:** if tableau is slow, use extracts instead of live connection
- **tooltips:** customize tooltips for each viz with relevant info
- **formatting:** use consistent fonts/colors across all sheets
- **filters:** add quick filters for date range, host, liquor type
- **actions:** set up dashboard actions for cross-filtering
- **mobile:** create mobile layout version if needed

---

## advanced: calculated fields

**cocktails per host:**
```
COUNTD([Cocktail])
```

**% of total:**
```
COUNTD([Cocktail]) / TOTAL(COUNTD([Cocktail]))
```

**classic vs modern:**
```
IF [Year Invented] < 1980 THEN "Classic"
ELSE "Modern"
END
```

**decade:**
```
FLOOR([Year Invented]/10)*10
```

---

## troubleshooting

**map not showing:**
- verify lat/lon are numeric
- check for null values
- use edit locations if tableau doesn't recognize cities

**bars not stacking:**
- analysis > stack marks > on
- verify measure is using count not sum

**overlapping labels:**
- reduce font size
- use label > allow labels to overlap
- or remove labels and rely on tooltips

**colors not matching:**
- edit colors > manually assign
- use stepped color or continuous scale as needed

---

## files you need

- `cocktail_history_tableau.csv` - main data file with all columns
- this guide

that's it. the csv has everything tableau needs (lat/lon, era buckets, etc).
