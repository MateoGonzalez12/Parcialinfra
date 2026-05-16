from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "flask-api"})

@app.route('/status')
def status():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "ok", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 500

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM items;")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "nombre": r[1]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)