from django.test import TestCase

# Create your tests here.
class LoginPageTestCase(TestCase):
    """ Check success or fail login """
    def test_login_page_returns_302(self):
        """ Test that the function returns the page with response 302 """
        pass
    
class RegisterPageTestCase(TestCase):
    """ Check success or fail registration """
    def test_registration_page_returns_302(self):
        """ Test that the function returns the page with response 302 """
        pass