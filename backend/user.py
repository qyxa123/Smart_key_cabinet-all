from flask import Blueprint, request
from extensions import db
from models import User, Key, BorrowRecord
from schemas import user_schema, users_schema, borrow_record_schema, borrow_records_schema
from datetime import datetime, timedelta

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
    reason = request.json.get('reason')
    
    if key_id is None:
        return {'error': 'key_id is required'}, 400
    if not reason or not reason.strip():
        return {'error': 'reason is required'}, 400
        
    try:
        key_id = int(key_id)
    except (TypeError, ValueError):
        return {'error': 'key_id must be integer'}, 400
        
    key = Key.query.get_or_404(key_id)
    
    # 检查钥匙是否已被借用（查看是否有未归还的记录）
    existing_record = BorrowRecord.query.filter_by(
        key_id=key_id, 
        status='borrowed'
    ).first()
    
    if existing_record:
        return {'error': f'钥匙已被 {existing_record.user.name} 借用'}, 400
    
    # 创建借用记录
    borrow_record = BorrowRecord(
        user_id=user.id,
        key_id=key_id,
        reason=reason.strip(),
        borrow_time=datetime.utcnow() + timedelta(hours=8),
        status='borrowed'
    )
    
    # 添加到多对多关系（保持兼容性）
    if key not in user.keys:
        user.keys.append(key)
    
    db.session.add(borrow_record)
    db.session.commit()
    
    return {
        'message': '钥匙借用成功',
        'user': user_schema.dump(user),
        'borrow_record': borrow_record_schema.dump(borrow_record)
    }

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
    
    # 查找未归还的借用记录
    borrow_record = BorrowRecord.query.filter_by(
        user_id=user.id,
        key_id=key_id,
        status='borrowed'
    ).first()
    
    if not borrow_record:
        return {'error': '未找到该用户的借用记录'}, 400
    
    # 更新借用记录
    borrow_record.return_time = datetime.utcnow() + timedelta(hours=8)
    borrow_record.status = 'returned'
    
    # 从多对多关系中移除（保持兼容性）
    if key in user.keys:
        user.keys.remove(key)
    
    db.session.commit()
    
    return {
        'message': '钥匙归还成功',
        'user': user_schema.dump(user),
        'borrow_record': borrow_record_schema.dump(borrow_record)
    }

# GET /user/<id>/borrow-records 获取用户的借用记录
@user_bp.route('/<int:id>/borrow-records', methods=['GET'])
def get_user_borrow_records(id):
    user = User.query.get_or_404(id)
    records = user.borrow_records.order_by(BorrowRecord.borrow_time.desc()).all()
    return borrow_records_schema.jsonify(records)

# GET /user/borrow-records 获取所有借用记录
@user_bp.route('/borrow-records', methods=['GET'])
def get_all_borrow_records():
    records = BorrowRecord.query.order_by(BorrowRecord.borrow_time.desc()).all()
    return borrow_records_schema.jsonify(records)

# GET /user/borrow-records/active 获取当前未归还的借用记录
@user_bp.route('/borrow-records/active', methods=['GET'])
def get_active_borrow_records():
    records = BorrowRecord.query.filter_by(status='borrowed').order_by(BorrowRecord.borrow_time.desc()).all()
    return borrow_records_schema.jsonify(records)

