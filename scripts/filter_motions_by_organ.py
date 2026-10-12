#!/usr/bin/env python3
"""
Filter parliamentary motions by committee (organ) and output to CSV.
"""

import json
import csv
from pathlib import Path


def load_json_file(filepath):
    """Load JSON file, handling encoding issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except:
            return None


def extract_motion_data(data):
    """Extract organ and date from motion JSON."""
    if 'dokumentstatus' not in data:
        return None

    doc = data['dokumentstatus'].get('dokument', {})
    organ = doc.get('organ', '')
    datum = doc.get('datum', '')

    return {
        'organ': organ,
        'datum': datum
    }


def find_matching_motions(data_dir, target_organ):
    """Find all motions matching the target organ."""
    matching_motions = []
    data_path = Path(data_dir)

    for folder in sorted(data_path.glob('mot-*')):
        if not folder.is_dir():
            continue

        for json_file in sorted(folder.glob('*.json')):
            data = load_json_file(str(json_file))
            if data is None:
                continue

            motion_data = extract_motion_data(data)
            if motion_data is None:
                continue

            organ = motion_data.get('organ', '')
            if organ and organ.upper() == target_organ.upper():
                matching_motions.append({
                    'filename': json_file.name,
                    'date': motion_data['datum']
                })

    return matching_motions


def save_to_csv(motions, output_file):
    """Save motion data to CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'date'])
        writer.writeheader()
        writer.writerows(motions)


def main():
    # Configuration
    TARGET_ORGAN = 'UbU'  # Hardcoded organ to filter by
    DATA_DIR = '/Users/rebecca/Dev/SU/Proj_course/data'
    OUTPUT_FILE = f'filtered_motions_{TARGET_ORGAN}.csv'

    print(f"Filtering motions with organ: {TARGET_ORGAN}")
    motions = find_matching_motions(DATA_DIR, TARGET_ORGAN)

    print(f"Found {len(motions)} motions")
    save_to_csv(motions, OUTPUT_FILE)
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
