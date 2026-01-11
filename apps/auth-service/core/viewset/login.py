from rest_framework import viewsets, status
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class LogoutViewSet(GenericViewSet):
    @action(detail=False, methods=["post"], url_path="logout", url_name="logout")
    def logout(self, request: Request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        request.session.flush()
        return response


@renderer_classes([TemplateHTMLRenderer])
class LoginViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["get"], url_path="login", url_name="login")
    def scan_action(self, request):
        return Response(template_name="login.html")
