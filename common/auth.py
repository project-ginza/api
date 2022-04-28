import json
from ginza.redis import redis_conn
from rest_framework.authentication import TokenAuthentication
from user.models import User


class RedisTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        user_data = redis_conn.get(key)
        if user_data is None:
            return None

        user = json.loads(user_data)
        user_obj = User()
        for key_name in user.keys():
            setattr(user_obj, key_name, user[key_name])
        return user_obj, key