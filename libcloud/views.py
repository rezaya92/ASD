import json
import mimetypes
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from ASD import settings
from libcloud.models import Content, Attachment
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def homePageView(request):
    context = {}
    context.update({'files': get_files()})
    return render(request=request, template_name='libcloud/intro.html',context = context)

def get_files():
    files = Content.objects.order_by('creator')[:1]
    return files

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")

            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name='libcloud/register.html', context={"register_form": form},
                      status=400)
    form = NewUserForm()
    return render(request=request, template_name='libcloud/register.html', context={"register_form": form} ,status=200)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return render(request=request, template_name="libcloud/login.html", context={"login_form": form},status=401)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request=request, template_name="libcloud/login.html", context={"login_form": form} ,status=401)
    form = AuthenticationForm()
    return render(request=request, template_name="libcloud/login.html", context={"login_form": form})


def file_page(request, filename):
    if request.method == "GET":
        contents = Content.objects.filter(file=filename).all()
        content = None
        if contents.count() == 1:
            content = contents[0]
        elif contents.count() == 0:
            if len(filename.split("/")) > 1:
                filename = filename.split("/")[-1]
            content = Content.objects.create(creator=request.user, type=Content.ContentType.Book,
                                             file=SimpleUploadedFile(filename, b"Test File"))
            content.contentfeature_set.create(name="feature1", value="value1")
            content.attachment_set.create(type=Attachment.AttachmentType.Subtitle,
                                          file=SimpleUploadedFile("attachment1.txt", b"Test attachment"))
            return redirect(f"/file_page/{content.file.name}")
        else:
            raise Exception
        return render(request, 'libcloud/file_page.html', {'file': content})


def download_file(request, user_prefix, filename):
    if request.method == "GET":
        file_path = os.path.join(settings.MEDIA_ROOT, user_prefix, filename)

        if not os.path.exists(file_path):
            messages.error(request, f"{filename} doesn't exists.")
            return redirect("/")

        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response


@login_required
def upload_file(request):
    pass


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
