from flask import Blueprint, request
from extensions import db
from models import User, Key
from schemas import user_schema, users_schema

user_bp = Blueprint('user', __name__)

# GET /user 列表
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

# POST /user 创建
@user_bp.route('/', methods=['POST'])
def create_user():
    user = user_schema.load(request.json)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

# GET /user/<id> 查询
@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user)

# PUT /user/<id> 更新
@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    user = user_schema.load(request.json, instance=user)
    db.session.commit()
    return user_schema.jsonify(user)

# DELETE /user/<id> 删除
@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# POST /user/<id>/borrow 借钥匙
@user_bp.route('/<int:id>/borrow', methods=['POST'])
def borrow_key(id):
    user = User.query.get_or_404(id)
    key_id = request.json.get('key_id')
    if key_id is None:
        return {'error': 'key_id is required'}, 400
    try:
        key_id = int(key_id)
    except (TypeError, ValueError):
        return {'error': 'key_id must be integer'}, 400
    key = Key.query.get_or_404(key_id)
    if key in user.keys:
        return {'error': 'key already borrowed'}, 400
    user.keys.append(key)
    db.session.commit()
    return user_schema.jsonify(user)

# POST /user/<id>/return 还钥匙
@user_bp.route('/<int:id>/return', methods=['POST'])
def return_key(id):
    user = User.query.get_or_404(id)
    key_id = request.json.get('key_id')
    if key_id is None:
        return {'error': 'key_id is required'}, 400
    try:
        key_id = int(key_id)
    except (TypeError, ValueError):
        return {'error': 'key_id must be integer'}, 400
    key = Key.query.get_or_404(key_id)
    if key not in user.keys:
        return {'error': 'key not borrowed by this user'}, 400
    user.keys.remove(key)
    db.session.commit()
    return user_schema.jsonify(user)

