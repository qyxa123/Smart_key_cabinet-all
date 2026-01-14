from models import User, Key, BorrowRecord
from extensions import ma
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = User
		include_relationships = True
		load_instance = True

class KeySchema(ma.SQLAlchemyAutoSchema):
	is_borrowed = fields.Boolean(dump_only=True)
	borrower_name = fields.String(dump_only=True)
	
	class Meta:
		model = Key
		include_relationships = True
		load_instance = True

class BorrowRecordSchema(ma.SQLAlchemyAutoSchema):
	user = fields.Nested(UserSchema, exclude=('keys', 'borrow_records'))
	key = fields.Nested(KeySchema, exclude=('users', 'borrow_records'))
	
	class Meta:
		model = BorrowRecord
		include_relationships = True
		load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
key_schema = KeySchema()
keys_schema = KeySchema(many=True)
borrow_record_schema = BorrowRecordSchema()
borrow_records_schema = BorrowRecordSchema(many=True)
