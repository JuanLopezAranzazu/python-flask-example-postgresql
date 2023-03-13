from .main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'created_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
