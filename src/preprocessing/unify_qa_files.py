import json
import hashlib

def generate_id(doc):
    combined = f"{doc['document']}-{'\n'.join(doc['patterns'])}-{'\n'.join(doc['responses'])}"
    hash_object = hashlib.md5(combined.encode())
    document_id = hash_object.hexdigest()
    print(document_id)
    return document_id


with open("data/500 Data Science Interview Questions.json", "r") as file:
    ds_qa = json.load(file)


with open("data/intents.json", "r") as file:
    cs_qa = json.load(file)


for qa in ds_qa:
    qa["patterns"] = qa.pop("question")
    qa["patterns"] = [qa["patterns"]]
    qa["responses"] = qa.pop("answer")
    qa["responses"] = [qa["responses"]]
    qa["document"] = "Book 500 Data Science Interview Questions by Vamsee Puligadda"
    qa['id'] = generate_id(qa)

cs_qa = cs_qa["intents"]
for qa in cs_qa:
    qa["document"] = "https://www.kaggle.com/datasets/mujtabamatin/computer-science-theory-qa-dataset"
    qa['id'] = generate_id(qa)

union_qa = cs_qa + ds_qa

with open("data/all_qa.json", "w") as file:
    json.dump(union_qa, file)