from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    # 初始化扩展
    db.init_app(app)
    ma.init_app(app)
