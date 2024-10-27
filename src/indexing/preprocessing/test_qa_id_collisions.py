import json
from collections import defaultdict


with open("data/all_qa_cleaned.json", "r") as file:
    union_qa = json.load(file)

hashes = defaultdict(list)

for doc in union_qa:
    doc_id = doc['id']
    hashes[doc_id].append(doc)

print(len(hashes), len(union_qa))
