from django.contrib import admin

from libcloud.models import Content, ContentFeature, Attachment, Library, ContentType

admin.site.register(Content)
admin.site.register(ContentFeature)
admin.site.register(Attachment)
admin.site.register(Library)
admin.site.register(ContentType)
