from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

app_name = "api"

v1_router = DefaultRouter()

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet)

urlpatterns = [
    path("", include(v1_router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]