from django.contrib import admin

from libcloud.models import Content, ContentFeature, Attachment, AttachmentType, ContentTypeFeature, ContentType

admin.site.register(Content)
admin.site.register(ContentFeature)
admin.site.register(Attachment)
admin.site.register(AttachmentType)
admin.site.register(ContentType)
admin.site.register(ContentTypeFeature)
