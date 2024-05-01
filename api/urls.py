from django.urls import include, path
from rest_framework import routers

from . import views


class BulkRouter(routers.DefaultRouter):
    """
    Map http methods to actions defined for bulk patch method.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routes[0].mapping.update(
            {
                "patch": "partial_bulk_update",
            }
        )


router = BulkRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

# app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
