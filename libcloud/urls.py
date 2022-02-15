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
    path(settings.MEDIA_URL + "<str:user_prefix>/<str:filename>", views.download_file, name="download_file"),
    # path("upload_success", views.upload_success, name="upload_success"),
]
