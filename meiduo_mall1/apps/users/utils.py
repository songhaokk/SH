from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
def email_token(id, email):
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = {"id": id,
            "email": email
            }
    data = serializer.dumps(data).decode()
    return 'http://www.meiduo.site:8000/semail/?token=%s'%(data)
def check_token(token):
    serilaizer = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        data = serilaizer.loads(token)
    except BadData:
        return None
    # return data
    id = data.get("id")
    email = data.get("email")
    return id, email
