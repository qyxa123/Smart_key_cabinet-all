from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟数据
users_data = [
    {
        "id": 1,
        "name": "张三",
        "identity": "student",
        "grade": "高一",
        "class_": "1班",
        "office": None,
        "keys": [{"id": 1, "room": "101"}]
    },
    {
        "id": 2,
        "name": "李老师",
        "identity": "teacher",
        "grade": None,
        "class_": None,
        "office": "办公室A",
        "keys": []
    }
]

keys_data = [
    {"id": 1, "room": "101", "users": [{"id": 1, "name": "张三", "identity": "student"}]},
    {"id": 2, "room": "102", "users": []},
    {"id": 3, "room": "201", "users": []},
    {"id": 4, "room": "202", "users": []}
]

@app.route("/")
def home():
    return '''
    <h1>智能钥匙柜管理系统后端API (简化版)</h1>
    <p>API接口已启动，前端请访问: <a href="http://localhost:3000">http://localhost:3000</a></p>
    <h2>可用接口:</h2>
    <ul>
        <li>GET /api/user/ - 获取所有用户</li>
        <li>POST /api/user/ - 创建用户</li>
        <li>GET /api/key/ - 获取所有钥匙</li>
        <li>POST /api/key/ - 创建钥匙</li>
        <li>POST /api/user/&lt;id&gt;/borrow - 借钥匙</li>
        <li>POST /api/user/&lt;id&gt;/return - 还钥匙</li>
    </ul>
    '''

# 用户相关API
@app.route('/api/user/', methods=['GET'])
def get_users():
    return jsonify(users_data)

@app.route('/api/user/', methods=['POST'])
def create_user():
    data = request.json
    new_user = {
        "id": len(users_data) + 1,
        "name": data.get('name'),
        "identity": data.get('identity'),
        "grade": data.get('grade'),
        "class_": data.get('class_'),
        "office": data.get('office'),
        "keys": []
    }
    users_data.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users_data if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users_data if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    user.update({
        "name": data.get('name', user['name']),
        "identity": data.get('identity', user['identity']),
        "grade": data.get('grade', user['grade']),
        "class_": data.get('class_', user['class_']),
        "office": data.get('office', user['office'])
    })
    return jsonify(user)

@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users_data
    users_data = [u for u in users_data if u['id'] != user_id]
    return '', 204

@app.route('/api/user/<int:user_id>/borrow', methods=['POST'])
def borrow_key(user_id):
    user = next((u for u in users_data if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    key_id = request.json.get('key_id')
    key = next((k for k in keys_data if k['id'] == key_id), None)
    if not key:
        return jsonify({"error": "Key not found"}), 404
    
    # 检查钥匙是否已被借用
    if any(u['id'] == user_id for u in key['users']):
        return jsonify({"error": "Key already borrowed by this user"}), 400
    
    # 借用钥匙
    user_info = {"id": user['id'], "name": user['name'], "identity": user['identity']}
    key_info = {"id": key['id'], "room": key['room']}
    
    user['keys'].append(key_info)
    key['users'].append(user_info)
    
    return jsonify(user)

@app.route('/api/user/<int:user_id>/return', methods=['POST'])
def return_key(user_id):
    user = next((u for u in users_data if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    key_id = request.json.get('key_id')
    key = next((k for k in keys_data if k['id'] == key_id), None)
    if not key:
        return jsonify({"error": "Key not found"}), 404
    
    # 检查用户是否借用了这把钥匙
    user_key = next((k for k in user['keys'] if k['id'] == key_id), None)
    if not user_key:
        return jsonify({"error": "Key not borrowed by this user"}), 400
    
    # 归还钥匙
    user['keys'] = [k for k in user['keys'] if k['id'] != key_id]
    key['users'] = [u for u in key['users'] if u['id'] != user_id]
    
    return jsonify(user)

# 钥匙相关API
@app.route('/api/key/', methods=['GET'])
def get_keys():
    return jsonify(keys_data)

@app.route('/api/key/', methods=['POST'])
def create_key():
    data = request.json
    new_key = {
        "id": len(keys_data) + 1,
        "room": data.get('room'),
        "users": []
    }
    keys_data.append(new_key)
    return jsonify(new_key), 201

@app.route('/api/key/<int:key_id>', methods=['GET'])
def get_key(key_id):
    key = next((k for k in keys_data if k['id'] == key_id), None)
    if key:
        return jsonify(key)
    return jsonify({"error": "Key not found"}), 404

@app.route('/api/key/<int:key_id>', methods=['PUT'])
def update_key(key_id):
    key = next((k for k in keys_data if k['id'] == key_id), None)
    if not key:
        return jsonify({"error": "Key not found"}), 404
    
    data = request.json
    key['room'] = data.get('room', key['room'])
    return jsonify(key)

@app.route('/api/key/<int:key_id>', methods=['DELETE'])
def delete_key(key_id):
    global keys_data
    key = next((k for k in keys_data if k['id'] == key_id), None)
    if not key:
        return jsonify({"error": "Key not found"}), 404
    
    # 检查钥匙是否被借用
    if key['users']:
        return jsonify({"error": "Key is currently borrowed"}), 400
    
    keys_data = [k for k in keys_data if k['id'] != key_id]
    return '', 204

if __name__ == "__main__":
    print("🔑 启动智能钥匙柜管理系统后端...")
    print("📱 前端地址: http://localhost:3000")
    print("🔧 后端API: http://localhost:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)