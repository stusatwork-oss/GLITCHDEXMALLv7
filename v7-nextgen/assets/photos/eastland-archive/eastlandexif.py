import os
from PIL import Image

directory = '.'  # Current directory

for filename in os.listdir(directory):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
        filepath = os.path.join(directory, filename)
        try:
            with Image.open(filepath) as img:
                exif_data = img._getexif()
                if exif_data:
                    print(f"--- {filename} ---")
                    for tag_id, value in exif_data.items():
                        # Decode the tag names for better readability
                        tag_name = Image.TAGS.get(tag_id, tag_id)
                        print(f"{tag_name}: {value}")
                else:
                    print(f"--- {filename} --- No EXIF data found.")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")