import jwt
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from core.models import Users
from core.util.token_generator import generate_app_token
from line.services.line_services import LineService


class RefreshTokenViewSet(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["post"], url_path="refresh", url_name="refresh")
    def post(self, request: Request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({
                "detail": "Missing refresh token",
                "login_url": LineService.create_login_url(request)
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({"detail": "refresh_expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "refresh_invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get("sub") or payload.get("user_id")
        try:
            user = Users.objects.get(id=user_id)
            token = generate_app_token(user)
            return Response({
                "access": token
            }, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({"detail": "user_not_found"}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError:
            return Response({
                "detail": "Refresh token expire",
                "login_url": LineService.create_login_url(request)
            }, status=status.HTTP_401_UNAUTHORIZED)
