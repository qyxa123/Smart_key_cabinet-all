from flask import Blueprint, request
from extensions import db
from models import Key
from schemas import key_schema, keys_schema

key_bp = Blueprint('key', __name__)

# GET /key 列表
@key_bp.route('/', methods=['GET'])
def get_keys():
    keys = Key.query.all()
    return keys_schema.jsonify(keys)

# POST /key 创建
@key_bp.route('/', methods=['POST'])
def create_key():
    key = key_schema.load(request.json)
    db.session.add(key)
    db.session.commit()
    return key_schema.jsonify(key), 201

# GET /key/<id> 查询
@key_bp.route('/<int:id>', methods=['GET'])
def get_key(id):
    key = Key.query.get_or_404(id)
    return key_schema.jsonify(key)

# PUT /key/<id> 更新
@key_bp.route('/<int:id>', methods=['PUT'])
def update_key(id):
    key = Key.query.get_or_404(id)
    key = key_schema.load(request.json, instance=key)
    db.session.commit()
    return key_schema.jsonify(key)

# DELETE /key/<id> 删除
@key_bp.route('/<int:id>', methods=['DELETE'])
def delete_key(id):
    key = Key.query.get_or_404(id)
    db.session.delete(key)
    db.session.commit()
    return '', 204

