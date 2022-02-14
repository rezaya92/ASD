import os

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from libcloud.models import Content, ContentFeature, Attachment


class ContentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testemail@gmail.com', username='username', password='123')

        with open('temp.txt', 'w') as f:
            f.write("Test File")
        return super().setUp()

    def tearDown(self):
        os.remove("temp.txt")

    def test_correct_content_create(self):
        with open('temp.txt', 'r') as f:
            Content.objects.create(creator=self.user, type=Content.ContentType.Book, file=File(f, 'temp.txt'))

    def test_content_create_with_null_creator(self):
        with open('temp.txt', 'r') as f:
            with self.assertRaises(ValidationError):
                Content.objects.create(type=Content.ContentType.Book, file=File(f, 'temp.txt'))

    def test_content_create_with_null_type(self):
        with open('temp.txt', 'r') as f:
            with self.assertRaises(ValidationError):
                Content.objects.create(creator=self.user, file=File(f, 'temp.txt'))

    def test_content_create_with_null_file(self):
        with self.assertRaises(ValidationError):
            Content.objects.create(creator=self.user, type=Content.ContentType.Book)
