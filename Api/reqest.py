import requests
import json
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
set_parent_dir = sys.path.append(parent_dir)

from models.tags import Tags

# x = Tags(name="fun")
# x.save()

item = "Books"
url = f'http://localhost:5600/add/{item}'

data = {
    "attr": {'name': 'تعلم c++ في 5 ايام', "author": "ahmed", "path": "test"},
    "tags": ["educational", "fun"]}

# Sending JSON data
headers = {'Content-Type': 'application/json'}
r = requests.post(url, headers=headers, data=json.dumps(data))

print(r.status_code)
print(r.content)
item = "tags"
url = f'http://localhost:5600/add/{item}'

r = requests.post(url, headers=headers, data=json.dumps(
    {"attr": {"name": "action"}}))

print(r.status_code)
print(r.content)
