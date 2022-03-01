import os
import shutil
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.conf import settings
from libcloud.models import Content, ContentFeature, Attachment, ContentType, AttachmentType, ContentTypeFeature, \
    Library

test_media_root = os.path.join(settings.BASE_DIR, 'test_media/')


@override_settings(MEDIA_ROOT=test_media_root)
class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')
        self.content_type = ContentType.objects.create(user=self.user, name='type1')
        self.content_file = SimpleUploadedFile('temp.txt', b"Test File")
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_content_create(self):
        Content.objects.create(creator=self.user, type=self.content_type,
                               file=self.content_file)

    def test_content_create_with_null_creator(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(type=self.content_type, file=self.content_file)

    def test_content_create_with_null_type(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(creator=self.user, file=self.content_file)

    def test_content_create_with_null_file(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(creator=self.user, type=self.content_type)


@override_settings(MEDIA_ROOT=test_media_root)
class ContentFeatureModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')
        self.content_type = ContentType.objects.create(user=self.user, name='type1')
        self.feature_type = ContentTypeFeature.objects.create(content_type=self.content_type,
                                                              name="abc",
                                                              type=ContentTypeFeature.FeatureType.Number,
                                                              required=True)
        self.content = Content.objects.create(creator=self.user, type=self.content_type,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_content_feature_create(self):
        ContentFeature.objects.create(content=self.content, feature_type=self.feature_type, value="1")

    def test_content_feature_create_with_null_content(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(feature_type=self.feature_type, value="1")

    def test_content_feature_create_with_null_feature_type(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(content=self.content, value="1")

    def test_content_feature_create_with_null_value(self):
        with self.assertRaises(ValidationError):
            ContentFeature.objects.create(content=self.content, feature_type=self.feature_type)

    def test_content_delete_cascade(self):
        feature = ContentFeature.objects.create(content=self.content, feature_type=self.feature_type, value="1")

        self.content.delete()
        with self.assertRaises(ContentFeature.DoesNotExist):
            ContentFeature.objects.get(id=feature.id)


@override_settings(MEDIA_ROOT=test_media_root)
class AttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')
        self.content_type = ContentType.objects.create(user=self.user, name='type1')
        self.content = Content.objects.create(creator=self.user, type=self.content_type,
                                              file=SimpleUploadedFile('vid.mp4', b"3242"))

        self.attachtype = AttachmentType.objects.create(user=self.user, name="attachtype1")

        self.attachment_file = SimpleUploadedFile('attachment.txt', b"Hello")
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_correct_attachment_create(self):
        Attachment.objects.create(content=self.content, type=self.attachtype,
                                  file=self.attachment_file)

    def test_attachment_create_with_null_type(self):
        with self.assertRaises(ValidationError):
            Attachment.objects.create(content=self.content, file=self.attachment_file)

    def test_attachment_create_with_null_file(self):
        with self.assertRaises(ValidationError):
            Attachment.objects.create(content=self.content, type=self.attachtype)

    def test_content_delete_cascade(self):
        attachment = Attachment.objects.create(content=self.content, type=self.attachtype,
                                               file=self.attachment_file)

        self.content.delete()
        with self.assertRaises(Attachment.DoesNotExist):
            Attachment.objects.get(id=attachment.id)


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = '/register/'
        self.login_url = '/login/'
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'Fineline94$',
            'password2': 'Fineline94$'
        }
        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'tes',
            'password2': 'tes',

        }
        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'teslatt',
            'password2': 'teslatto',

        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password1': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libcloud/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_withshortpassword(self):
        response = self.client.post(self.register_url, self.user_short_password, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 400)


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libcloud/login.html')

    def test_login_success(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.login_url, {
            'username': self.user.get('username'),
            'password': self.user.get('password1')}, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_cantlogin_with_unverified_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.login_url, {
            'username': 'wrong',
            'password': 'wrong'}, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_cantlogin_with_no_username(self):
        response = self.client.post(self.login_url, {'password': 'passwped', 'username': ''}, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_cantlogin_with_no_password(self):
        response = self.client.post(self.login_url, {'username': 'passwped', 'password': ''}, format='text/html')
        self.assertEqual(response.status_code, 401)


@override_settings(MEDIA_ROOT=test_media_root)
class DownloadFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')
        self.content_type = ContentType.objects.create(user=self.user, name='type1')
        self.content = Content.objects.create(creator=self.user, type=self.content_type,
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
class ContentPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')
        self.content_type = ContentType.objects.create(user=self.user, name='type1')
        self.content = Content.objects.create(creator=self.user, type=self.content_type,
                                              file=SimpleUploadedFile('temp.txt', b"Test File"))

        self.content_page_url = '/content'
        super().setUp()

    def tearDown(self):
        if os.path.exists(test_media_root):
            shutil.rmtree(test_media_root)
        super().tearDown()

    def test_content_page_success(self):
        # print(f"{self.file_page_url}/{self.content.file.name}")
        response = self.client.get(f"{self.content_page_url}/{self.content.id}")
        self.assertEqual(response.status_code, 200)

    # TODO


class AttachmentTypeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', username='username', password='123')
        self.attachment_types_url = '/my_attachment_types/'
        self.attachment_type1 = AttachmentType.objects.create(user=self.user, name="a_type1")
        self.attachment_type2 = AttachmentType.objects.create(user=self.user, name="a_type2")
        self.client.login(username='username', password='123')

    def test_my_attachment_types_success(self):
        response = self.client.get(self.attachment_types_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['attachment_types'].count(), 2)
        self.assertEqual(response.context['attachment_types'][0].name, self.attachment_type1.name)
        self.assertEqual(response.context['attachment_types'][1].name, self.attachment_type2.name)

    def test_create_attachment_type(self):
        response = self.client.post(self.attachment_types_url, {"name": "a_type3"}, format='text/html')
        self.assertEqual(response.status_code, 200)
        attachment_types = self.user.attachmenttype_set.all()
        self.assertEqual(attachment_types.count(), 3)
        self.assertEqual(attachment_types[2].name, "a_type3")


class CreateContentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', username='username', password='123')
        self.create_content_url = '/content/create/'

        self.content_type1 = ContentType.objects.create(user=self.user, name='c_type1')
        self.content_type2 = ContentType.objects.create(user=self.user, name='c_type2')

        self.library1 = Library.objects.create(user=self.user, name='lib1', content_type=self.content_type1)
        self.library2 = Library.objects.create(user=self.user, name='lib2', content_type=self.content_type2)

        self.client.login(username='username', password='123')

    def test_content_create_page_data(self):
        response = self.client.get(self.create_content_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].fields['type'].queryset.all().count(), 2)
        self.assertEqual(response.context['form'].fields['type'].queryset[0].name, self.content_type1.name)

        self.assertEqual(response.context['form'].fields['library'].queryset.all().count(), 2)
        self.assertEqual(response.context['form'].fields['library'].queryset[0].name, self.library1.name)

    def test_content_create_page_data_with_multiple_users(self):
        user2 = User.objects.create_user(email='testemail2@gmail.com', username='username2', password='123456')
        content_type1_user2 = ContentType.objects.create(user=user2, name='c_type1_user2')
        library1_user2 = Library.objects.create(user=user2, name='lib1_user2', content_type=content_type1_user2)

        response = self.client.get(self.create_content_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].fields['type'].queryset.all().count(), 2)
        self.assertEqual(response.context['form'].fields['type'].queryset[0].name, self.content_type1.name)

        self.assertEqual(response.context['form'].fields['library'].queryset.all().count(), 2)
        self.assertEqual(response.context['form'].fields['library'].queryset[0].name, self.library1.name)
