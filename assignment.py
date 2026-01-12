import json

with open('precipitation.json', encoding='utf-8') as file:
    data = json.load(file)

print(data)