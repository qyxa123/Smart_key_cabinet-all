from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    # 先初始化扩展，确保 db/ma 绑定到 app
    db.init_app(app)
    ma.init_app(app)
    # 延迟导入蓝图，避免在模块导入阶段产生循环依赖
    from user import user_bp
    from key import key_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(key_bp, url_prefix='/key')
