#pylint: disable=C0103, W0612
""" Python testing file checking that user profile is updated"""
from django.contrib.auth.models import User
from django import forms
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile
from PIL import Image
from django.core.files.base import File

class UserCreationFormTest(TestCase):

    def test_user_already_exists(self):
        data = {
            'username': 'jacob',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())

class TestUpdateProfile(TestCase):
    """Class checking that profile update contains no bug"""
    def setUp(self):
       # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.form_data = {'username': 'jacob123',
                    'email': 'jacob123@gmail.com',
                }

    def test_update_userdata_is_valid(self):
        """ function testing that username and email are updated"""
        self.client.login(username='jacob', password='top_secret')
        u_form = UserUpdateForm(self.form_data)   
        u_form.save()
        response = self.client.post(reverse('profile'), self.form_data)
        self.assertTrue(u_form.is_valid())
        self.user.username = 'jacob123'
        self.user.email = 'jacob123@gmail.com'
        self.assertContains(response, 'jacob123')
        self.assertContains(response, 'jacob123@gmail.com')
        self.assertEqual(response.status_code, 200)

    def test_update_userdata_is_not_valid(self):
        """ function testing that username and email are not valid"""
        self.client.login(username='jacob', password='top_secret')
        form_data2 = {'username': '',
                    'email': 'jacob123ail.com',
                }
        u_form = UserUpdateForm(form_data2)
        self.assertFalse(u_form.is_valid())
        response = self.client.post(reverse('profile'), form_data2)
        self.assertTemplateUsed(response, 'users/profile.html')

class UploadImageTests(TestCase):
    def test_valid_form(self):
        '''valid post data should redirect the expected behavior is to show the image'''
        self.client.login(username='jacob', password='top_secret')
        formdata = {}
        with open('purbeurre/media/profile_pics/remy.png', 'rb') as f:
            formdata['image'] = f
            response = self.client.post(reverse('profile'), formdata)
        p_form = ProfileUpdateForm(f)
        self.assertEqual(response.status_code, 302)

    # def test_not_valid_form(self):
    #     '''valid post data should not redirect the expected behavior is to show the image'''
    #     self.client.login(username='jacob', password='top_secret')
    #     formdata = {}
    #     with open('purbeurre/users/__init__.py', 'rb') as f:
    #         formdata['image'] = f
    #         response = self.client.post(reverse('profile'), formdata)
    #     p_form = ProfileUpdateForm(f)
    #     self.assertEqual(response.status_code, 302)
