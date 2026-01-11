from rest_framework import routers

from core.viewset.login import LoginViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", LoginViewSet, basename="login-template")

urlpatterns = router.urls
