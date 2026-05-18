#!/bin/bash
set -e

yum update -y
yum install -y python3 python3-pip git

pip3 install flask psycopg2-binary gunicorn

# Clonar app
git clone https://github.com/MateoGonzalez12/Parcialinfra.git /app
cd /app/app

# Escribir variables en archivo que persiste para el servicio
cat > /etc/app.env <<EOF
DB_HOST=${db_host}
DB_NAME=${db_name}
DB_USER=${db_user}
DB_PASSWORD=${db_password}
EOF

# Esperar a que la DB esté disponible (hasta 5 minutos)
echo "Esperando base de datos..."
for i in $(seq 1 30); do
  python3 -c "
import psycopg2
conn = psycopg2.connect(
  host='${db_host}',
  database='${db_name}',
  user='${db_user}',
  password='${db_password}'
)
conn.close()
" && break
  echo "Intento $i fallido, reintentando en 10s..."
  sleep 10
done

# Crear tabla
python3 -c "
import psycopg2
conn = psycopg2.connect(
  host='${db_host}',
  database='${db_name}',
  user='${db_user}',
  password='${db_password}'
)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, nombre TEXT);')
cur.execute(\"INSERT INTO items (nombre) VALUES ('item-demo') ON CONFLICT DO NOTHING;\")
conn.commit()
conn.close()
"

# Crear servicio systemd
cat > /etc/systemd/system/flaskapp.service <<EOF
[Unit]
Description=Flask App
After=network.target

[Service]
EnvironmentFile=/etc/app.env
WorkingDirectory=/app/app
ExecStart=/usr/local/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable flaskapp
systemctl start flaskapp