from flask import Flask, request, jsonify, render_template
import math
import sqlite3

app = Flask(__name__)

# Opprett database ved første kjøring
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS skudd (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skytter TEXT,
        skive TEXT,
        x REAL,
        y REAL,
        poeng INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

def beregn_poeng(x, y):
    avstand = math.sqrt(x**2 + y**2)
    if avstand <= 0.5:
        return 11
    for i in range(10, 0, -1):
        if avstand <= i:
            return i
    return 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrer_skudd", methods=["POST"])
def registrer_skudd():
    data = request.json
    skytter = data["skytter"]
    skive = data["skive"]
    x = data["x"]
    y = data["y"]
    poeng = beregn_poeng(x, y)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO skudd (skytter, skive, x, y, poeng) VALUES (?, ?, ?, ?, ?)",
              (skytter, skive, x, y, poeng))
    conn.commit()
    conn.close()

    return jsonify({"poeng": poeng})

@app.route("/hent_resultater", methods=["GET"])
def hent_resultater():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT skytter, skive, x, y, poeng FROM skudd")
    rows = c.fetchall()
    conn.close()

    resultater = {}
    for skytter, skive, x, y, poeng in rows:
        if skytter not in resultater:
            resultater[skytter] = {}
        if skive not in resultater[skytter]:
            resultater[skytter][skive] = []
        resultater[skytter][skive].append({"x": x, "y": y, "poeng": poeng})

    return jsonify(resultater)

if __name__ == "__main__":
    app.run(debug=True)