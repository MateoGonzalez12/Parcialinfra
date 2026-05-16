#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install flask psycopg2-binary gunicorn

# Variables de entorno
export DB_HOST="${db_host}"
export DB_NAME="${db_name}"
export DB_USER="${db_user}"
export DB_PASSWORD="${db_password}"

# Clonar app desde GitHub (ajusta la URL)
git clone https://github.com/MateoGonzalez12/Parcialinfra.git /app
cd /app/app

# Crear tabla de ejemplo
python3 -c "
import psycopg2, os
conn = psycopg2.connect(host=os.environ['DB_HOST'],database=os.environ['DB_NAME'],user=os.environ['DB_USER'],password=os.environ['DB_PASSWORD'])
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, nombre TEXT);')
cur.execute(\"INSERT INTO items (nombre) VALUES ('item-demo') ON CONFLICT DO NOTHING;\")
conn.commit(); conn.close()
"

# Levantar con gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 app:app --daemon