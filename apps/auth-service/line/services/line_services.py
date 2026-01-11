import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request

from core.exception.line_exception import LineServiceUnavailable
from core.models import Users
from core.util.password_generator import generate_password
from line.dataclass.line import LineAccess


class LineService:
    Header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_MESSAGE_ACCESS_TOKEN}",
    }

    @classmethod
    def get_access_from_code(cls, code: str) -> str:
        res = Request.post(settings.LINE_GET_TOKEN,
                           data=LineAccess.get_data(code).to_data(),
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
        res_data = res.json()
        if res.status_code != status.HTTP_200_OK:
            raise LineServiceUnavailable(res_data)
        access_token = res_data.get("access_token")
        if not access_token:
            raise LineServiceUnavailable("No access_token from LINE response")
        return access_token

    @classmethod
    def get_user_from_access_token(cls, token: str) -> Users:
        profile_res = Request.get("https://api.line.me/v2/profile", headers={
            "Authorization": f"Bearer {token}"
        })
        profile = profile_res.json()

        line_user_id = profile.get("userId")
        display_name = profile.get("displayName", "DISPLAY_NAME_NOT_FOUND")
        profile_img_url = profile.get("pictureUrl", "PROFILE_IMG_URL_NOT_FOUND")
        profile_img_url = f"{profile_img_url}/small"

        if not line_user_id:
            raise LineServiceUnavailable("No userId in line token")

        try:
            user = Users.objects.get(line_user_id=line_user_id)
        except Users.DoesNotExist:
            user = Users.objects.create_user(
                username=f"line_{line_user_id}",
                password=generate_password(12),
                line_user_id=line_user_id,
                first_name=display_name,
                name=display_name,
                profile_img_url=profile_img_url
            )
        return user

    @classmethod
    def create_login_url(cls, request: Request) -> str:
        state = str(uuid.uuid4())
        request.session['line_login_state'] = state
        login_url = settings.LINE_LOGIN_URL.format(
            client_id=settings.LINE_LOGIN_CLIENT_ID,
            redirect_uri=settings.LINE_LOGIN_REDIRECT_URI,
            state=state
        )
        return login_url
