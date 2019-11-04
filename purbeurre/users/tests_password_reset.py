#pylint: disable=C0103, W0612
""" Python testing file checking each page returns the correct response"""
from django.test import TestCase
from django.core import mail
from django.urls import reverse, resolve

class TestMailSent(TestCase):
    """ testing class used to confirm that an email is sent """
    def setUp(self):
        """ method used to confirm that an email is sent """
        mail.send_mail(
            'Réinitialisation du mot de passe sur 127.0.0.1:8000', 'Vous recevez \
            ce message en réponse à votre demande de réinitialisation du mot\
            de passe de votre compte sur 127.0.0.1:8000.',
            'lymickael91@gmail.com', ['lymickael91@gmail.com'],
            fail_silently=False,
        )

    def test_password_reset_page(self):
            """test that to the Password Reset page that must return HTTP 200 and
            the right template that shows the email form.
            """
            response = self.client.get(reverse('password_reset'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'users/password_reset.html')


    def test_mail_is_sent(self):
        """ Test that one message has been sent. """
        self.assertEqual(len(mail.outbox), 1)

    def test_mail_is_sent_with_the_right_subject(self):
        """ Verify that the subject of the message is correct. """
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation du mot de passe sur 127.0.0.1:8000')

    def test_mail_is_sent_with_right_email(self):
        """ Check that a mail the user is redirected after recognized email"""
        response = self.client.post(reverse('password_reset'), {'email':'lymickael91@gmail.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/password-reset/done/')

    def test_password_is_reset(self):
        """ check that the new password page is ok """
        response = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}))
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}), data={'new_password1':'Testing321', 'new_password2':'Testing321'})
        self.assertEqual(response2.status_code, 200)

    def test_password_not_complete(self):
        response = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}), data={'new_password1':'Testing321', 'new_password2':'Abdcdfdfd321'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_reset_confirm.html')

    