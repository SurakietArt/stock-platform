import uuid
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.util.token_generator import generate_app_token
from line.services.line_services import LineService

User = get_user_model()


class LineViewSet(GenericViewSet):
    authentication_classes = []

    @action(detail=False, methods=["get"], url_path="login", url_name="login")
    def line_login(self, request: Request) -> Response:
        return redirect(LineService.create_login_url(request))

    @action(detail=False, methods=["get"], url_path="callback", url_name="callback")
    def line_callback(self, request: Request) -> Response:
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or state != request.session.get("line_login_state"):
            return Response(data="Invalid request", status=status.HTTP_400_BAD_REQUEST)
        line_access_token = LineService.get_access_from_code(code)
        user = LineService.get_user_from_access_token(line_access_token)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        token = generate_app_token(user)
        params = urlencode({
            "access": token,
            "name": user.first_name,
            "user_image_url": user.profile_img_url
        })
        response = redirect(f"{settings.FRONTEND_REDIRECT_URL}?{params}")

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=settings.REFRESH_TOKEN_LIFE_TIME
        )

        return response

    @action(detail=False, methods=["post"], url_path="webhook", url_name="webhook")
    def line_webhook(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK)


@renderer_classes([TemplateHTMLRenderer])
class LineTemplateViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=["get"], url_path="callback", url_name="callback")
    def line_call_back(self, request):
        return Response(template_name="line_callback.html")

