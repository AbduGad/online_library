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
    'name': 'bit manipulation', "author": "Alx Africa",
    "tags": ["educational", "fun"]
}


file = {'pdf': open('/mnt/s/alx/online_library/bit_manipulation.pdf', 'rb')}
with open('/mnt/s/alx/online_library/bit_manipulation.pdf', 'rb') as file:
    r = requests.post(
        url,

        data=data,
        files={'pdf': file})

print(r.status_code)
print(r.content)
