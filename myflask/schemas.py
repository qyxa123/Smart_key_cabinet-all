from models import User, Key
from extensions import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = User
		include_relationships = True
		load_instance = True

class KeySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Key
		include_relationships = True
		load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
key_schema = KeySchema()
keys_schema = KeySchema(many=True)
