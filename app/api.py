from flask import jsonify, request, abort
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

@app.route('/api/users', methods=['GET'])
def get_users():
    """Получить список всех пользователей."""
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    """Создать нового пользователя."""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    """Получить информацию о пользователе по ID."""
    user = db.session.get(User, id)
    if not user:
        abort(404)
    return jsonify({'id': user.id, 'username': user.username})

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Обновить данные пользователя."""
    user = db.session.get(User, id)
    if not user:
        abort(404)
    data = request.get_json()
    if 'username' in data:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Удалить пользователя."""
    user = db.session.get(User, id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})