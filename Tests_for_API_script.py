import requests
import json
import sqlite3

# Add some entries to database and print database
with sqlite3.connect('wikidb.db') as conn:
    cur = conn.cursor()
    example1 = ('Example Title 1', 'Content for example title 1') 
    example2 = ('Example Title 2', 'Content for example title 2')
    cur.execute("INSERT INTO wikidata(title, content) VALUES(?,?)", example1)
    cur.execute("INSERT INTO wikidata(title, content) VALUES(?,?)", example2)
    cur.execute("SELECT * FROM wikidata") 
    rows = cur.fetchall()
    print(rows)
    

# GET tests
response = requests.get("http://127.0.0.1:5000/documents")
print(response.status_code)
print(response.json())

response = requests.get("http://127.0.0.1:5000/documents/Example Title 1")
print(response.status_code)
print(response.json())

# POST tests
update = {"content": "posted content3"} 
resp = requests.post("http://127.0.0.1:5000/documents/Example Title3", json=update) # ie. invalid title
print(resp.status_code)
print(resp._content) 

update = {"content": "new posted content"}
resp = requests.post("http://127.0.0.1:5000/documents/Example Title 2", json=update)
print(resp.status_code)
print(resp._content)

# Print updated database
with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM wikidata")
    rows = cur.fetchall()
    print(rows)