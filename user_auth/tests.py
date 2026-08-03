from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import RegistrationForm


class RegistrationFormTests(TestCase):
    def test_valid_username_creates_user(self):
        form = RegistrationForm(
            data={
                'username': 'newuser',
                'password1': 'strong-pass-123',
                'password2': 'strong-pass-123',
            }
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_mismatched_passwords_invalid(self):
        form = RegistrationForm(
            data={
                'username': 'newuser',
                'password1': 'strong-pass-123',
                'password2': 'different-pass-123',
            }
        )
        self.assertFalse(form.is_valid())


class RegisterViewTests(TestCase):
    def test_get_renders_register_page(self):
        response = self.client.get(reverse('user_auth:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

    def test_post_valid_registration_creates_user_and_redirects(self):
        response = self.client.post(
            reverse('user_auth:register'),
            {
                'username': 'newuser',
                'password1': 'strong-pass-123',
                'password2': 'strong-pass-123',
            },
        )
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('user_auth:login'))

    def test_post_invalid_registration_rerenders_page(self):
        response = self.client.post(
            reverse('user_auth:register'),
            {
                'username': 'newuser',
                'password1': 'short',
                'password2': 'different',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='test-pass-123'
        )

    def test_get_renders_login_page(self):
        response = self.client.get(reverse('user_auth:login'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_credentials_logs_in(self):
        response = self.client.post(
            reverse('user_auth:login'),
            {'username': 'tester', 'password': 'test-pass-123'},
        )
        self.assertRedirects(response, reverse('home'))

    def test_post_invalid_credentials_rerenders_page(self):
        response = self.client.post(
            reverse('user_auth:login'),
            {'username': 'tester', 'password': 'wrong-pass'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Logged in')


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='test-pass-123'
        )

    def test_logout_logs_out_and_redirects_home(self):
        self.client.login(username='tester', password='test-pass-123')
        response = self.client.get(reverse('user_auth:logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )
