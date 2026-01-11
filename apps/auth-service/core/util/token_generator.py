from datetime import timedelta, datetime, UTC

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_app_token(user: User):
    payload = {
        "sub": str(user.id),
        "line_user_id": user.line_user_id,
        "name": user.first_name,
        "exp": datetime.now(tz=UTC) + timedelta(hours=settings.TOKEN_LIFE_TIME),
        "iat": datetime.now(tz=UTC)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def issue_token_response(user: User):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({
        "access": access_token,
        "user": {
            "id": user.id,
            "name": user.first_name,
        }
    })

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=settings.REFRESH_TOKEN_LIFE_TIME
    )
    return response
