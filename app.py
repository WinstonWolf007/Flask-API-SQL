from flask import Flask, request
import json
import sqlite3


app = Flask(__name__)


@app.route("/create", methods=["POST"])
def create():
    conn = sqlite3.connect("players.db")
    cur = conn.cursor()
    
    #param
    req = request.get_json()

    for var in req:
        cur.execute(f"INSERT INTO user (name, value) VALUES ('{var}', '{req.get(var)}')")
    
    conn.commit()
    conn.close()

    return json.dumps({"status": "OK"})

@app.route("/display", methods=["POST"])
def display():
    conn = sqlite3.connect("players.db")
    cur = conn.cursor()
    
    #param
    name = request.get_json().get("name")

    cur.execute(f"SELECT value FROM user WHERE name='{name}'")
    result = cur.fetchall()
    conn.commit()
    conn.close()

    if result:
        return str(result[0][0])
    else:
        return "null"
    
@app.route("/remove", methods=["POST"])
def remove():
    conn = sqlite3.connect("players.db")
    cur = conn.cursor()
    
    #param
    name = request.get_json().get("name")

    cur.execute(f"DELETE FROM user WHERE name='{name}'")
    conn.commit()
    conn.close()

    return json.dumps({"status": "OK"})

    
if __name__ == "__main__":
    # Reset table
    conn = sqlite3.connect("players.db")
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS "user"''')
    cur.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), value VARCHAR(50))''')
    conn.commit()
    conn.close()

    app.run()
