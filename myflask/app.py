import sys
import os

# Add local Flask-Admin to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Flask-Admin', 'flask-admin'))

from flask import Flask
from flask_cors import CORS
from extensions import db, ma, init_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Key
from user import user_bp
from key import key_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for Flask-Admin sessions

# Enable CORS for frontend
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/school?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(key_bp, url_prefix='/api/key')

# Flask-Admin setup
admin = Admin(app, name='School Management')
admin.add_view(ModelView(User, db.session, name='User Admin', endpoint='user_admin'))
admin.add_view(ModelView(Key, db.session, name='Key Admin', endpoint='key_admin'))

# Auto-create tables on startup
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return '''
    <h1>智能钥匙柜管理系统后端API</h1>
    <p>API接口已启动，前端请访问: <a href="http://localhost:3000">http://localhost:3000</a></p>
    <p>管理后台: <a href="/admin">Flask Admin</a></p>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
