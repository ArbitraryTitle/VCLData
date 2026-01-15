#!/usr/bin/env python3
"""
Script to sort all cocktail timeline tables in the PowerPoint by year
"""
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import shutil
import zipfile

# Define namespaces
namespaces = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a16': 'http://schemas.microsoft.com/office/drawing/2014/main'
}

# Register namespaces to preserve them in output
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

def process_slide(slide_file):
    """Process a single slide and extract table data"""
    tree = ET.parse(slide_file)
    root = tree.getroot()

    # Find the table
    table = root.find('.//a:tbl', namespaces)
    if table is None:
        return None, None

    # Extract all rows
    rows = table.findall('.//a:tr', namespaces)
    if len(rows) < 2:
        return None, None

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
            if date_obj:
                row_data.append({
                    'row_element': row,
                    'num': num,
                    'date': date_str,
                    'date_obj': date_obj,
                    'mc': mc,
                    'cocktail': cocktail,
                    'selections': selections,
                    'year': date_obj.year,
                    'slide': slide_file.name
                })

    return (tree, table, header_row, data_rows, row_data)

def main():
    extract_dir = Path('/home/user/VCLData/pptx_extract')
    slides_dir = extract_dir / 'ppt' / 'slides'

    # Process all history slides
    slide_files = [
        slides_dir / f'slide{n}.xml'
        for n in [38, 39, 40, 41, 42, 43, 44]
    ]

    all_row_data = []
    slide_info = {}

    # Extract all data from all slides
    print("Extracting data from all slides...")
    for slide_file in slide_files:
        if not slide_file.exists():
            continue

        result = process_slide(slide_file)
        if result[0] is None:
            continue

        tree, table, header_row, data_rows, row_data = result
        slide_info[slide_file] = {
            'tree': tree,
            'table': table,
            'header_row': header_row,
            'data_rows': data_rows
        }
        all_row_data.extend(row_data)
        print(f"  {slide_file.name}: {len(row_data)} rows")

    print(f"\nTotal rows extracted: {len(all_row_data)}")

    # Sort all data by year and date
    sorted_data = sorted(all_row_data, key=lambda x: (x['year'], x['date_obj']))

    print("\nSorted cocktails by year:")
    current_year = None
    for i, item in enumerate(sorted_data, 1):
        if item['year'] != current_year:
            current_year = item['year']
            print(f"\n  === {current_year} ===")
        print(f"  {i}. {item['date']} - {item['cocktail']}")

    # Distribute sorted data across slides (10 rows per slide)
    rows_per_slide = 10

    for i, slide_file in enumerate(slide_files):
        if slide_file not in slide_info:
            continue

        start_idx = i * rows_per_slide
        end_idx = start_idx + rows_per_slide
        slide_data = sorted_data[start_idx:end_idx]

        if not slide_data:
            break

        info = slide_info[slide_file]
        table = info['table']

        # Update row numbers
        for j, item in enumerate(slide_data, start=start_idx + 1):
            row = item['row_element']
            cells = row.findall('.//a:tc', namespaces)
            if cells:
                first_cell = cells[0]
                text_elem = first_cell.find('.//a:t', namespaces)
                if text_elem is not None:
                    text_elem.text = str(j)

        # Remove all data rows from table
        for row in info['data_rows']:
            table.remove(row)

        # Add sorted rows back
        for item in slide_data:
            table.append(item['row_element'])

        # Write back to file
        info['tree'].write(slide_file, encoding='UTF-8', xml_declaration=True)
        print(f"\nUpdated {slide_file.name} with rows {start_idx + 1}-{end_idx}")

    # Repack the PowerPoint file
    print("\nRepacking PowerPoint file...")
    pptx_file = Path('/home/user/VCLData/64-2025-05-22 VCL Meeting.pptx')
    backup_file = Path('/home/user/VCLData/64-2025-05-22 VCL Meeting_backup.pptx')

    # Create backup
    shutil.copy2(pptx_file, backup_file)
    print(f"Created backup: {backup_file}")

    # Create new PPTX file
    with zipfile.ZipFile(pptx_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in extract_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(extract_dir)
                zipf.write(file_path, arcname)

    print(f"Updated PowerPoint file: {pptx_file}")
    print("\nDone! The cocktail timeline is now sorted by year.")

if __name__ == '__main__':
    main()
