from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from apiapi.models import *
from apiapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users",Users,"user")
router.register(r"categories",CategoryViewSet, basename="category")
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print([url.name for url in router.urls])