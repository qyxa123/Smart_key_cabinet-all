from extensions import db
from datetime import datetime

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
	student_id = db.Column(db.String(20))  # 学号或工号
	grade = db.Column(db.String(10))
	class_ = db.Column(db.String(10))
	office = db.Column(db.String(10))
	
	#多对多关系：一个用户可以借多把钥匙
	keys = db.relationship('Key', secondary=JNFLSIC_keys, back_populates='users', lazy='joined')
	
	#一对多关系：一个用户可以有多条借用记录
	borrow_records = db.relationship('BorrowRecord', back_populates='user', lazy='dynamic')
	
	def __repr__(self):
		return f"<User {self.name}>"

#钥匙表
class Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	room = db.Column(db.String(10), nullable=False)

	#多对多关系：一把钥匙可以被多个用户借过
	users = db.relationship('User', secondary=JNFLSIC_keys, back_populates='keys', lazy='joined')
	
	#一对多关系：一把钥匙可以有多条借用记录
	borrow_records = db.relationship('BorrowRecord', back_populates='key', lazy='dynamic')
	
	@property
	def is_borrowed(self):
		# 检查是否有未归还的借用记录
		return self.borrow_records.filter_by(status='borrowed').count() > 0

	@property
	def borrower_name(self):
		record = self.borrow_records.filter_by(status='borrowed').first()
		return record.user.name if record else None

	def __repr__(self):
		return f"<Key {self.room}>"

#借用记录表
class BorrowRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	key_id = db.Column(db.Integer, db.ForeignKey('key.id'), nullable=False)
	reason = db.Column(db.Text, nullable=False)  # 借用理由
	borrow_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 借用时间
	return_time = db.Column(db.DateTime)  # 归还时间，为空表示未归还
	status = db.Column(db.String(20), nullable=False, default='borrowed')  # borrowed, returned
	
	#外键关系
	user = db.relationship('User', back_populates='borrow_records')
	key = db.relationship('Key', back_populates='borrow_records')

	@property
	def user_name(self):
		return self.user.name

	@property
	def key_room(self):
		return self.key.room
	
	def __repr__(self):
		return f"<BorrowRecord {self.user.name} - {self.key.room} - {self.status}>"