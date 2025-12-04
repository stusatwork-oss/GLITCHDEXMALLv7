#!/usr/bin/env python3

import os
import json
import sys

# Instructions:
# 1. Ensure that the eastland-archive directory is in the correct location relative to this script.
# 2. Run this script from the terminal using: python3 create_symlinks_batches_1_2_3.py

# Define batch file paths
batches = [
    'BATCH_1_CLASSIFICATION_MANIFEST.json', 
    'BATCH_2_CLASSIFICATION_MANIFEST.json', 
    'BATCH_3_CLASSIFICATION_MANIFEST.json'
]

# Define directory names
zones_dir = 'zones/'
semantic_dir = 'semantic/'
narrative_dir = 'narrative/'

# Create directories if they don't exist
for directory in [zones_dir, semantic_dir, narrative_dir]:
    os.makedirs(directory, exist_ok=True)

# Function to create symlinks
def create_symlinks(batch_file):
    with open(batch_file) as f:
        data = json.load(f)
        for photo in data['photos']:
            filename = photo['filename']
            categories = photo.get('categories', [])

            try:
                for zone in photo['zones']:
                    zone_path = os.path.join(zones_dir, zone)
                    os.symlink(f'../../eastland-archive/{filename}', zone_path)
                    print(f'Created symlink: {zone_path} -> ../../eastland-archive/{filename}')

                for semantic in categories.get('semantic', []):
                    semantic_path = os.path.join(semantic_dir, semantic)
                    os.symlink(f'../../eastland-archive/{filename}', semantic_path)
                    print(f'Created symlink: {semantic_path} -> ../../eastland-archive/{filename}')

                for narrative in categories.get('narrative', []):
                    narrative_path = os.path.join(narrative_dir, narrative)
                    os.symlink(f'../../eastland-archive/{filename}', narrative_path)
                    print(f'Created symlink: {narrative_path} -> ../../eastland-archive/{filename}')
            except Exception as e:
                print(f'Error creating symlink for {filename}: {e}')

# Iterate through batches
for batch in batches:
    try:
        create_symlinks(batch)
    except Exception as e:
        print(f'Failed to process batch {batch}: {e}')

print('All operations completed. Check above for logs of created symlinks and any errors.')