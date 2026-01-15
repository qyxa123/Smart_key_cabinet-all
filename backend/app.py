import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add local Flask-Admin to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Flask-Admin', 'flask-admin'))

from flask import Flask
from flask_cors import CORS
from flask_babel import Babel
from extensions import db, ma, init_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired
from models import User, Key, BorrowRecord
from user import user_bp
from key import key_bp

class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        user_count = User.query.count()
        key_count = Key.query.count()
        active_borrow_count = BorrowRecord.query.filter_by(status='borrowed').count()
        recent_records = BorrowRecord.query.order_by(BorrowRecord.borrow_time.desc()).limit(5).all()
        
        return self.render('admin/index.html', 
                           user_count=user_count,
                           key_count=key_count,
                           active_borrow_count=active_borrow_count,
                           recent_records=recent_records)

class UserModelView(ModelView):
    column_searchable_list = ['name', 'identity']
    column_filters = ['identity', 'grade']
    column_labels = {'name': '姓名', 'identity': '身份', 'grade': '年级', 'class_': '班级', 'office': '办公室'}

class KeyModelView(ModelView):
    column_searchable_list = ['room']
    column_labels = {'room': '房间号'}

class BorrowRecordModelView(ModelView):
    column_list = ('user', 'key', 'reason', 'borrow_time', 'return_time', 'status')
    column_labels = {'user': '借用人', 'key': '钥匙', 'reason': '理由', 'borrow_time': '借用时间', 'return_time': '归还时间', 'status': '状态'}
    column_filters = ['status', 'borrow_time']
    can_create = False
    
    form_columns = ('user', 'key', 'reason', 'borrow_time', 'return_time', 'status')
    form_args = {
        'user': {'validators': [DataRequired()]},
        'key': {'validators': [DataRequired()]},
        'reason': {'validators': [DataRequired()]}
    }

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
app.config.setdefault('BABEL_DEFAULT_LOCALE', 'zh_CN')
babel = Babel(app)

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
admin = Admin(app, name='智能钥匙柜管理后台', index_view=DashboardView(), template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session, name='用户管理', endpoint='user_admin'))
admin.add_view(KeyModelView(Key, db.session, name='钥匙管理', endpoint='key_admin'))
admin.add_view(BorrowRecordModelView(BorrowRecord, db.session, name='借用记录', endpoint='borrow_record_admin'))

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
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    print(f"🔧 Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
