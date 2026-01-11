from rest_framework import routers

from line.viewset.line_viewset import LineTemplateViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", LineTemplateViewSet, basename="line-template")

urlpatterns = router.urls
