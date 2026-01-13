import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')

# Enable CORS for frontend
CORS(app)

# Database configuration - use environment variable or fallback to SQLite for development
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # Fallback to SQLite for development if no DATABASE_URL is set
    database_url = 'sqlite:///school.db'
    print("Warning: Using SQLite fallback. Set DATABASE_URL environment variable for MySQL.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

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
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
