from flask import Flask, request, render_template, redirect, jsonify
import sqlite3

app = Flask(__name__)

# 🔧 Initialisation correcte de la base
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
        mode TEXT,
        source TEXT DEFAULT 'unknown'
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM drone_data ORDER BY timestamp DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return render_template('dashboard.html', data=rows)

@app.route('/update_location', methods=['POST'])
def receive_data():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    print(f"Données Flutter reçues : {data}")
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO drone_data (latitude, longitude, source) VALUES (?, ?, ?)",
              (latitude, longitude, 'flutter'))
    conn.commit()
    conn.close()
    return {'status': 'ok'}

@app.route('/last_position', methods=['GET'])
def last_position():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM drone_data WHERE source='flutter' ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({'latitude': row[0], 'longitude': row[1]})
    else:
        return jsonify({'error': 'no data'}), 404

@app.route('/reset', methods=['POST'])
def reset_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM drone_data")
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
# TEST