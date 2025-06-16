import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db
from app.models import User

@pytest.fixture
def client():
    """Фикстура для тестового клиента с чистой базой данных."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def logged_in_client(client):
    """Фикстура для авторизованного клиента."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    return client

def test_get_users_empty(client):
    """Тест получения пустого списка пользователей."""
    rv = client.get('/api/users')
    assert rv.status_code == 200
    assert rv.json == []

def test_create_user(client):
    """Тест создания нового пользователя."""
    rv = client.post('/api/users', json={'username': 'testuser', 'password': 'testpass'})
    assert rv.status_code == 201
    assert rv.json['username'] == 'testuser'

def test_create_user_duplicate(client):
    """Тест создания пользователя с уже существующим именем."""
    client.post('/api/users', json={'username': 'testuser', 'password': 'testpass'})
    rv = client.post('/api/users', json={'username': 'testuser', 'password': 'testpass2'})
    assert rv.status_code == 400
    assert 'error' in rv.json

def test_get_user(client):
    """Тест получения пользователя по ID."""
    client.post('/api/users', json={'username': 'testuser', 'password': 'testpass'})
    rv = client.get('/api/users/1')
    assert rv.status_code == 200
    assert rv.json['username'] == 'testuser'

def test_get_user_not_found(client):
    """Тест получения несуществующего пользователя."""
    rv = client.get('/api/users/999')
    assert rv.status_code == 404

def test_update_user(client):
    """Тест обновления данных пользователя."""
    client.post('/api/users', json={'username': 'testuser', 'password': 'testpass'})
    rv = client.put('/api/users/1', json={'username': 'newuser', 'password': 'newpass'})
    assert rv.status_code == 200
    assert rv.json['username'] == 'newuser'

def test_delete_user(client):
    """Тест удаления пользователя."""
    client.post('/api/users', json={'username': 'testuser', 'password': 'testpass'})
    rv = client.delete('/api/users/1')
    assert rv.status_code == 200
    assert rv.json['message'] == 'User deleted'
    rv = client.get('/api/users/1')
    assert rv.status_code == 404

def test_users_page(logged_in_client):
    """Тест рендеринга страницы пользователей."""
    rv = logged_in_client.get('/users')
    assert rv.status_code == 200
    response_data = rv.data.decode('utf-8')
    assert 'Управление пользователями' in response_data
    assert 'Добавить пользователя' in response_data
    assert 'Обновить пользователя' in response_data
    assert 'Удалить пользователя' in response_data
    assert '<ul id="user-list">' in response_data