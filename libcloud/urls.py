from django.conf.urls.static import static
from django.urls import path

from ASD import settings
from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.homePageView, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("file_page/<str:name>", views.file_page, name="file_page"),
    path("upload_file", views.upload_file, name="upload_file"),
]
