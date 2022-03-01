from django.conf.urls.static import static
from django.urls import path

from ASD import settings
from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.home_page_view, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("file_page/<path:filename>", views.file_page, name="file_page"),
    path("content/create/", views.create_content, name="create_content"),
    path("content/create/<int:content_type_pk>/", views.create_content, name="create_content_with_pk"),
    path("content/change_library/<int:pk>", views.LibraryChoiceView.as_view(), name="library_choice"),
    path(settings.MEDIA_URL + "<str:user_prefix>/<str:filename>", views.download_file, name="download_file"),
    path("libraries/", views.AllLibrariesView.as_view(), name="all_libraries"),
    path("libraries/<int:pk>/", views.EachLibraryView.as_view(), name="each_library"),
    path("libraries/create/", views.LibraryCreateView.as_view(), name="create_library"),
    path("my_content/", views.MyContentView.as_view(), name="my_content"),
    path("my_content_types/", views.my_content_types, name="my_content_types"),
    path("my_attachment_types/", views.my_attachment_types, name="my_attachment_types"),
    path("attachment_type/create/", views.AttachmentTypeCreateView.as_view(), name="create_attachment_type"),
    path("attachment/create/<int:content_pk>/", views.AttachmentCreateView.as_view(), name="create_attachment"),
    path("content_type/create/", views.create_content_type, name="create_content_type"),
    path("content_type/<int:pk>/", views.EachContentTypeView.as_view(), name="each_content_type"),
    # path("upload_success", views.upload_success, name="upload_success"),
]
