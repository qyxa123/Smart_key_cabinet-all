from extensions import db

#多对多中间表
JNFLSIC_keys = db.Table('jnflsic_keys',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('key_id', db.Integer, db.ForeignKey('key.id'), primary_key=True)
	)

#用户表
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	identity = db.Column(db.String(10), nullable=False)
	grade = db.Column(db.String(10))
	class_ = db.Column(db.String(10))
	office = db.Column(db.String(10))
	
	#多对多关系：一个用户可以借多把钥匙
	keys = db.relationship('Key', secondary=JNFLSIC_keys, back_populates='users', lazy='joined')
	def __repr__(self):
		return f"<User {self.name}>"

#钥匙表
class Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	room = db.Column(db.String(10), nullable=False)

	#多对多关系：一把钥匙可以被多个用户借过
	users = db.relationship('User', secondary=JNFLSIC_keys, back_populates='keys', lazy='joined')
	def __repr__(self):
		return f"<Key {self.room}>"