from flask import Flask, jsonify, request
import psycopg2
import os
import socket
from datetime import datetime

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask API - Infraestructura AWS</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 40px; }
            h1 { color: #38bdf8; }
            .card { background: #1e293b; border-radius: 12px; padding: 24px; margin: 16px 0; border: 1px solid #334155; }
            .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }
            .ok { background: #166534; color: #4ade80; }
            .endpoint { color: #7dd3fc; font-family: monospace; font-size: 15px; }
            a { color: #38bdf8; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>🚀 Flask API — AWS Infrastructure</h1>
        <div class="card">
            <h3>Endpoints disponibles</h3>
            <p><span class="endpoint"><a href="/health">/health</a></span> — Estado del servicio</p>
            <p><span class="endpoint"><a href="/status">/status</a></span> — Conexión a base de datos</p>
            <p><span class="endpoint"><a href="/api/items">/api/items</a></span> — Listar items</p>
            <p><span class="endpoint"><a href="/info">/info</a></span> — Info del servidor</p>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "service": "flask-api",
        "timestamp": datetime.utcnow().isoformat(),
        "instance": socket.gethostname()
    })

@app.route('/status')
def status():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        conn.close()
        return jsonify({
            "status": "ok",
            "db": "connected",
            "db_version": version,
            "instance": socket.gethostname()
        })
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 500

@app.route('/info')
def info():
    return jsonify({
        "instance_id": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat(),
        "region": "us-east-1",
        "environment": "production"
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM items;")
    rows = cur.fetchall()
    conn.close()
    return jsonify({
        "instance": socket.gethostname(),
        "count": len(rows),
        "items": [{"id": r[0], "nombre": r[1]} for r in rows]
    })

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    nombre = data.get('nombre', 'sin nombre')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (nombre) VALUES (%s) RETURNING id;", (nombre,))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"id": new_id, "nombre": nombre}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)