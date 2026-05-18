import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

# ── Test 1: /health no necesita BD, prueba directa ──
def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'ok'

# ── Test 2: /status simula conexión exitosa a BD ──
def test_status_ok(client):
    with patch('app.get_db') as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ['PostgreSQL 15.0']
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        r = client.get('/status')
        assert r.status_code == 200
        data = r.get_json()
        assert data['db'] == 'connected'

# ── Test 3: /status simula fallo de BD ──
def test_status_db_error(client):
    with patch('app.get_db') as mock_db:
        mock_db.side_effect = Exception('connection refused')
        r = client.get('/status')
        assert r.status_code == 500

# ── Test 4: /api/items simula respuesta de BD ──
def test_get_items(client):
    with patch('app.get_db') as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 'item-demo'), (2, 'otro-item')]
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn

        r = client.get('/api/items')
        assert r.status_code == 200
        data = r.get_json()
        assert data['count'] == 2
        assert len(data['items']) == 2
        assert data['items'][0]['nombre'] == 'item-demo'