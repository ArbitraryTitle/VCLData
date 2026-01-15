#!/usr/bin/env python3
"""
Script to sort the cocktail timeline table in the PowerPoint by year
"""
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Define namespaces
namespaces = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a16': 'http://schemas.microsoft.com/office/drawing/2014/main'
}

# Register namespaces
for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)

def extract_text_from_cell(cell):
    """Extract text content from a table cell"""
    texts = []
    for text_elem in cell.findall('.//a:t', namespaces):
        if text_elem.text:
            texts.append(text_elem.text)
    return ''.join(texts)

def parse_date(date_str):
    """Parse date string and return datetime object"""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except:
        return None

def main():
    slide_file = Path('/home/user/VCLData/pptx_extract/ppt/slides/slide38.xml')

    # Parse XML
    tree = ET.parse(slide_file)
    root = tree.getroot()

    # Find the table
    table = root.find('.//a:tbl', namespaces)
    if table is None:
        print("Table not found!")
        return

    # Extract all rows
    rows = table.findall('.//a:tr', namespaces)

    # Separate header and data rows
    header_row = rows[0]
    data_rows = rows[1:]

    # Extract data from each row
    row_data = []
    for i, row in enumerate(data_rows):
        cells = row.findall('.//a:tc', namespaces)
        if len(cells) >= 4:
            num = extract_text_from_cell(cells[0])
            date_str = extract_text_from_cell(cells[1])
            mc = extract_text_from_cell(cells[2])
            cocktail = extract_text_from_cell(cells[3])
            selections = extract_text_from_cell(cells[4]) if len(cells) > 4 else ""

            date_obj = parse_date(date_str)
            row_data.append({
                'index': i,
                'row_element': row,
                'num': num,
                'date': date_str,
                'date_obj': date_obj,
                'mc': mc,
                'cocktail': cocktail,
                'selections': selections,
                'year': date_obj.year if date_obj else 0
            })

    print(f"Found {len(row_data)} data rows")
    print("\nOriginal order:")
    for item in row_data:
        print(f"  {item['num']}. {item['date']} - {item['cocktail']}")

    # Sort by year (and then by date within year)
    sorted_data = sorted(row_data, key=lambda x: (x['year'], x['date_obj']) if x['date_obj'] else (9999, None))

    print("\nSorted by year:")
    for i, item in enumerate(sorted_data, 1):
        print(f"  {i}. {item['date']} - {item['cocktail']}")

    # Update row numbers
    for i, item in enumerate(sorted_data, 1):
        # Find the first cell (number column) and update it
        row = item['row_element']
        cells = row.findall('.//a:tc', namespaces)
        if cells:
            first_cell = cells[0]
            text_elem = first_cell.find('.//a:t', namespaces)
            if text_elem is not None:
                text_elem.text = str(i)

    # Remove all data rows from table
    for row in data_rows:
        table.remove(row)

    # Add sorted rows back
    for item in sorted_data:
        table.append(item['row_element'])

    # Write back to file
    tree.write(slide_file, encoding='UTF-8', xml_declaration=True)
    print(f"\nUpdated {slide_file}")

if __name__ == '__main__':
    main()
