import os

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


def get_content_upload_path(instance, filename):
    return os.path.join(
        "user_%s" % instance.creator.username, filename)


class Content(Model):
    class ContentType(models.IntegerChoices):
        Video = 1
        Image = 2
        Text = 3
        Audio = 4
        Other = 5

    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    type = models.IntegerField(choices=ContentType.choices)
    file = models.FileField(upload_to=get_content_upload_path)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)


class ContentFeature(Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def get_attachment_upload_path(instance, filename):
    return "_".join(["%s" % os.path.splitext(instance.content.file.name)[0], filename])


class Attachment(Model):
    class AttachmentType(models.IntegerChoices):
        Subtitle = 1
        Other = 2

    content_to_attachment_map = {
        Content.ContentType.Video.label: {AttachmentType.Subtitle.label}
    }

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    type = models.IntegerField(choices=AttachmentType.choices)
    file = models.FileField(upload_to=get_attachment_upload_path)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.content.get_type_display() not in Attachment.content_to_attachment_map or self.get_type_display() not in \
                Attachment.content_to_attachment_map[self.content.get_type_display()]:
            errors["mismatch types"] = f"{self.content.get_type_display()} " \
                                       f"can not have {self.get_type_display()} attachment."
        if errors:
            raise ValidationError(errors)

    def filename(self):
        return os.path.basename(self.file.name)
