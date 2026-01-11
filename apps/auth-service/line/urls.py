from rest_framework import routers

from line.viewset.line_viewset import LineViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", LineViewSet, basename="line")

urlpatterns = router.urls
