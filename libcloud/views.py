import json
import mimetypes
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView

from libcloud.models import Content, Attachment, Library
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def homePageView(request):
    context = {}
    current_user = request.user
    if request.user.is_authenticated:
        my_filter_qs = Q()
        my_filter_qs = my_filter_qs | Q(creator=current_user)
        print(current_user)
        files = Content.objects.filter(my_filter_qs)[:3]
        context.update({'files': files})
    return render(request=request, template_name='libcloud/intro.html',context = context)

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
        # for c in contents:
        #     print(c.file.name)
        # print(len(contents))
        content = None
        if contents.count() == 1:
            content = contents[0]
        elif contents.count() == 0:
            # if len(filename.split("/")) > 1:
            #     filename = filename.split("/")[-1]
            # content = Content.objects.create(creator=request.user, type=Content.ContentType.Text,
            #                                  file=SimpleUploadedFile(filename, b"Test File"))
            # content.contentfeature_set.create(name="feature1", value="value1")
            # content.attachment_set.create(type=Attachment.AttachmentType.Subtitle,
            #                               file=SimpleUploadedFile("attachment1.txt", b"Test attachment"))
            # return redirect(f"/file_page/{content.file.name}")
            messages.info(request, f"{filename} doesn't exists.")
            return redirect("/")
        else:
            messages.error(request, "internal error")
            return redirect("/")
        return render(request, 'libcloud/file_page.html', {'file': content})
    else:
        return redirect('libcloud:file_page', filename)


def download_file(request, user_prefix, filename):
    if request.method == "GET":
        file_path = os.path.join(settings.MEDIA_ROOT, user_prefix, filename)
        if not os.path.exists(file_path):
            messages.error(request, f"{filename} doesn't exists.")
            return redirect("/")

        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type, status=200)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
    else:
        return redirect('libcloud:download_file', user_prefix, filename)


@login_required
def upload_file(request):
    pass


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


class AllLibrariesView(ListView):
    model = Library


class EachLibraryView(DetailView):

    model = Library


class LibraryCreateView(CreateView):

    model = Library
    fields = ['name', 'content_type']
