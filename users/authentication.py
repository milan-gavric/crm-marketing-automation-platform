import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = None

        # Check Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        elif not token:
            # Check cookies
            token = request.COOKIES.get('token')

        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get('id')
            if not user_id:
                raise AuthenticationFailed('Invalid token')

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')

            return (user, None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')


def generate_token(user):
    import jwt
    from django.conf import settings
    from datetime import datetime

    payload = {
        'id': str(user.id),
        'email': user.email,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.utcnow(),
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

