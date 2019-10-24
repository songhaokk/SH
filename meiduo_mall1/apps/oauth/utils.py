from itsdangerous import BadData
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
def generate_token(openid):
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = {"openid":openid}
    token = serializer.dumps(data)
    return token.decode()
def check_token(access_token):
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        return data.get("openid")