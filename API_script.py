from flask import Flask, request, jsonify, abort
import sqlite3
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# Create database and table
with sqlite3.connect('wikidb.db') as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS wikidata (title varchar(50) PRIMARY KEY, content text);")
conn.close()

@app.route('/documents', methods=['GET'])
def documents():
    with sqlite3.connect('wikidb.db') as conn: 
        cur = conn.cursor()
        cur.execute("SELECT title FROM wikidata") 
        rows = cur.fetchall()
    conn.close()  
     
    # Construct list
    list_of_titles = []
    for row in rows:
        list_of_titles.append(row[0])
            
    return jsonify(list_of_titles)

@app.route('/documents/<title>', methods=['GET','POST'])
def documents2(title):     
    if request.method == "GET":
        with sqlite3.connect('wikidb.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT content FROM wikidata WHERE title=?",(title,)) 
            content = cur.fetchall()
        conn.close()
        
        # Return error if no results returned
        if not content:
            return "Error: No such title exists in wiki", 400
        
        return jsonify(content[0][0])
        
    if request.method == "POST":
        incoming_python = request.get_json() 
        
        def validity_test(incoming_python):
            """ Check that the posted JSON is of the form {"content": "new content..."} """
            if type(incoming_python) != dict: return False
            if len(incoming_python) != 1: return False
            for key in incoming_python:
                if key != "content": return False 
            if type(incoming_python["content"]) != str: return False
            return True
        
        if not validity_test(incoming_python): 
            return "Error: Posted data must be in the format {'content': 'new content...'}", 400
        
        # Updating database 
        new_content = incoming_python["content"]
        
        with sqlite3.connect('wikidb.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT content FROM wikidata WHERE title=?",(title,))
            content = cur.fetchall()
            
            # Return error if title not in wiki
            if not content:
                return "Error: No such title exists in wiki.", 400
            
            cur.execute("UPDATE wikidata SET content=? WHERE title=?", (new_content,title))
        conn.close()
        return "Successful update", 201 

app.run()