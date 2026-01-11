from __future__ import annotations
from dataclasses import dataclass

from django.conf import settings
from django_dataclass_autoserialize import AutoSerialize


@dataclass
class LineAccess(AutoSerialize):
    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str

    @classmethod
    def example(cls) -> LineAccess:
        return cls(
            grant_type="authorization_code",
            code="code",
            redirect_uri="redirect_uri",
            client_id="client_id",
            client_secret="client_secret"
        )

    @classmethod
    def get_data(cls, code: str) -> LineAccess:
        return cls(
            grant_type="authorization_code",
            code=code,
            redirect_uri=settings.LINE_LOGIN_REDIRECT_URI,
            client_id=settings.LINE_LOGIN_CLIENT_ID,
            client_secret=settings.LINE_LOGIN_CHANNEL_SECRET
        )
