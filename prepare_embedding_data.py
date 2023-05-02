import csv
import json
import random
# Read gun data from CSV file
gun_data = []
with open('data/gun_data.csv', 'r', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        gun_data.append(row)

# Generate prompt and completion pairs
# prompt_completion_pairs = []
embedding_pairs = list()

for row in gun_data:
    raw = f"description for {row['Name']}?. Manufacture date for {row['Name']}?. How much is the {row['Name']}?. Do you have {row['Name']}?. The gun named {row['Name']} is manufactured by {row['Manufacturer']} and uses the {row['Cartridge']} cartridge. Created from {row['Country']} and produced in the year {row['Year']}. The {row['Name']} is wort {random.randint(1, 10000)} dollars with a discount of 30-40%. You can buy the {row['Name']} using this link: https://www.pbdionisio.com/product/crosman-pumpmaster-760-bkt/"
    embedding_pairs.append(raw)

# Print prompt and completion pairs
# for pair in prompt_completion_pairs:
#     print(pair)

with open('data/new_gun_data_for_embedding.csv', 'w') as f:
    f.write('context\n')
    for i in embedding_pairs:
        json.dump(i, f)
        f.write('\n')
