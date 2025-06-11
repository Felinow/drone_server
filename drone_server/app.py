from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS drone_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        speed REAL,
        mode TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM drone_data ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return render_template('dashboard.html', data=rows)

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Données reçues :", data)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO drone_data (latitude, longitude, altitude, speed, mode) VALUES (?, ?, ?, ?, ?)",
              (data['latitude'], data['longitude'], data['altitude'], data['speed'], data['mode']))
    conn.commit()
    conn.close()
    return {'status': 'ok'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
