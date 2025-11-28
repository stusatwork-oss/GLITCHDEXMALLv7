import json

b1 = json.load(open('BATCH_1_CLASSIFICATION_MANIFEST.json'))
b2 = json.load(open('BATCH_2_CLASSIFICATION_MANIFEST.json'))
b3 = json.load(open('BATCH_3_CLASSIFICATION_MANIFEST.json'))

print(f'Batch 1: {b1["total_items"]} items')
print(f'Batch 2: {b2["total_items"]} items')
print(f'Batch 3: {b3["total_items"]} items')
print(f'Total: {b1["total_items"]+b2["total_items"]+b3["total_items"]} items')
