import time
from typing import Optional, Tuple

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from core.exception.auth_exception import AuthUserNotFound, AuthenticationFailed
from core.models import Users


class JWTAuthenticationMiddleware(BaseAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[Users, str]]:
        # to avoid template path
        if not request.path.startswith("/api/"):
            return None
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationFailed("Authorization not found")
        auth_type, token = auth_header.split(" ")
        auth_type = auth_type.lower()
        if auth_type != "bearer":
            raise AuthenticationFailed("Invalid token type")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            line_user_id = payload.get("line_user_id", None)
            if line_user_id is None:
                raise AuthenticationFailed("Invalid token payload")

            try:
                user = Users.objects.get(line_user_id=line_user_id)
                request.user = user
                return user, ""
            except Users.DoesNotExist:
                raise AuthUserNotFound()

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token Expire")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
