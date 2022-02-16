import os
import shutil

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.conf import settings
from libcloud.models import Content, ContentFeature, Attachment

test_media_root = os.path.join(settings.BASE_DIR, 'test_media/')


@override_settings(MEDIA_ROOT=test_media_root)
class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        self.content_file = SimpleUploadedFile('temp.txt', b"Test File")
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_content_create(self):
        Content.objects.create(creator=self.user, type=Content.ContentType.Text,
                               file=self.content_file)

    def test_content_create_with_null_creator(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(type=Content.ContentType.Text, file=self.content_file)

    def test_content_create_with_null_type(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(creator=self.user, file=self.content_file)

    def test_content_create_with_null_file(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(creator=self.user, type=Content.ContentType.Text)


@override_settings(MEDIA_ROOT=test_media_root)
class ContentFeatureModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        self.content = Content.objects.create(creator=self.user, type=Content.ContentType.Text,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_content_feature_create(self):
        ContentFeature.objects.create(content=self.content, name="abc", value="x")

    def test_content_feature_create_with_null_content(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(name="abc", value="x")

    def test_content_feature_create_with_null_name(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(content=self.content, value="x")

    def test_content_feature_create_with_null_value(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(content=self.content, name="abc")

    def test_content_delete_cascade(self):
        feature = ContentFeature.objects.create(content=self.content, name="abc", value="x")

        self.content.delete()
        with self.assertRaises(ContentFeature.DoesNotExist):
            ContentFeature.objects.get(id=feature.id)


@override_settings(MEDIA_ROOT=test_media_root)
class AttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        self.content = Content.objects.create(creator=self.user, type=Content.ContentType.Text,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))

        self.attachment_file = SimpleUploadedFile('attachment.txt', b"Hello")
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_attachment_create(self):
        Attachment.objects.create(content=self.content, type=Attachment.AttachmentType.Subtitle,
                                  file=self.attachment_file)

    def test_attachment_create_with_null_content(self):
        with self.assertRaises(ValidationError):
            Attachment.objects.create(type=Attachment.AttachmentType.Subtitle,
                                      file=self.attachment_file)

    def test_attachment_create_with_null_type(self):
        with self.assertRaises(ValidationError):
            Attachment.objects.create(content=self.content, file=self.attachment_file)

    def test_attachment_create_with_null_file(self):
        with self.assertRaises(ValidationError):
            Attachment.objects.create(content=self.content, type=Attachment.AttachmentType.Subtitle)

    def test_content_delete_cascade(self):
        attachment = Attachment.objects.create(content=self.content, type=Attachment.AttachmentType.Subtitle,
                                               file=self.attachment_file)

        self.content.delete()
        with self.assertRaises(Attachment.DoesNotExist):
            Attachment.objects.get(id=attachment.id)


@override_settings(MEDIA_ROOT=test_media_root)
class DownloadFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        self.content = Content.objects.create(creator=self.user, type=Content.ContentType.Text,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))

        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_download_file_success(self):
        response = self.client.get(f"{self.content.file.url}")
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=temp.txt")
        self.assertEquals(response.content, b"Test File")

    def test_download_file_doesnt_exists(self):
        username = 'user_a'
        filename = 'file.txt'
        response = self.client.get(f"{settings.MEDIA_URL}{username}/{filename}")
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(f"{filename} doesn't exists.", messages)


@override_settings(MEDIA_ROOT=test_media_root)
class FilePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        self.content = Content.objects.create(creator=self.user, type=Content.ContentType.Text,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))

        self.file_page_url = '/file_page'
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_file_page_success(self):
        print(f"{self.file_page_url}/{self.content.file.name}")
        response = self.client.get(f"{self.file_page_url}/{self.content.file.name}")
        self.assertEqual(response.status_code, 200)

    # TODO

