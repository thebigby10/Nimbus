from datetime import date, timedelta
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import File
from .forms import PublicFileForm, AuthenticatedFileForm


def sample_file(name='sample.txt', content=b'hello nimbus'):
    return SimpleUploadedFile(name, content, content_type='text/plain')


class FileModelTests(TestCase):
    def test_file_str_is_title(self):
        file_obj = File.objects.create(
            title='My File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )
        self.assertEqual(str(file_obj), 'My File')

    def test_file_uses_uuid_primary_key(self):
        file_obj = File.objects.create(
            title='UUID File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=1),
        )
        self.assertIsInstance(file_obj.id, uuid.UUID)


class PublicFileFormTests(TestCase):
    def test_form_requires_only_uploaded_file(self):
        form = PublicFileForm(data={}, files={'uploaded_file': sample_file()})
        self.assertTrue(form.is_valid())

    def test_form_rejects_upload_without_file(self):
        form = PublicFileForm(data={})
        self.assertFalse(form.is_valid())


class PublicViewTests(TestCase):
    def test_get_renders_upload_page(self):
        response = self.client.get(reverse('file_shareapp:public_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload a New File')

    def test_post_uploads_file_and_sets_default_expiry(self):
        response = self.client.post(
            reverse('file_shareapp:public_view'),
            {'uploaded_file': sample_file()},
        )
        self.assertEqual(File.objects.count(), 1)
        file_obj = File.objects.first()
        self.assertEqual(file_obj.title, 'sample.txt')
        self.assertEqual(file_obj.user, None)
        self.assertEqual(
            file_obj.expiry_date, date.today() + timedelta(days=7)
        )
        self.assertRedirects(
            response,
            reverse('file_shareapp:file_detail_view', args=[file_obj.id]),
        )

    def test_post_without_file_rerenders_page(self):
        response = self.client.post(reverse('file_shareapp:public_view'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 0)


class AuthenticatedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='test-pass-123'
        )
        self.client.login(username='tester', password='test-pass-123')

    def test_auth_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('file_shareapp:auth_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_auth_upload_requires_login(self):
        self.client.logout()
        response = self.client.post(
            reverse('file_shareapp:auth_view'),
            {
                'uploaded_file': sample_file(),
                'title': 'My Upload',
                'expiry_date': '2026-12-31',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(File.objects.count(), 0)

    def test_post_uploads_file_owned_by_user(self):
        response = self.client.post(
            reverse('file_shareapp:auth_view'),
            {
                'uploaded_file': sample_file(),
                'title': 'My Upload',
                'expiry_date': '2026-12-31',
            },
        )
        self.assertEqual(File.objects.count(), 1)
        file_obj = File.objects.first()
        self.assertEqual(file_obj.user, self.user)
        self.assertEqual(file_obj.title, 'My Upload')
        self.assertEqual(file_obj.expiry_date, date(2026, 12, 31))
        self.assertRedirects(
            response,
            reverse('file_shareapp:file_detail_view', args=[file_obj.id]),
        )

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('file_shareapp:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_only_lists_own_files(self):
        other_user = User.objects.create_user(
            username='other', password='test-pass-123'
        )
        File.objects.create(
            user=other_user,
            title='Other File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )
        File.objects.create(
            user=self.user,
            title='My File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )
        response = self.client.get(reverse('file_shareapp:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My File')
        self.assertNotContains(response, 'Other File')


class FileDetailTests(TestCase):
    def test_file_detail_returns_page(self):
        file_obj = File.objects.create(
            title='Detail File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )
        response = self.client.get(
            reverse('file_shareapp:file_detail_view', args=[file_obj.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail File')

    def test_file_detail_404_for_missing_file(self):
        response = self.client.get(
            reverse('file_shareapp:file_detail_view', args=['00000000-0000-0000-0000-000000000000'])
        )
        self.assertEqual(response.status_code, 404)


class FileDownloadTests(TestCase):
    def setUp(self):
        self.file_obj = File.objects.create(
            title='Download File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )

    def test_download_returns_attachment(self):
        response = self.client.get(
            reverse('file_shareapp:file_download_view', args=[self.file_obj.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'].split(';')[0], 'attachment')
        self.assertEqual(b''.join(response.streaming_content), b'hello nimbus')

    def test_download_404_for_missing_file(self):
        file_id = self.file_obj.id
        self.file_obj.delete()
        response = self.client.get(
            reverse('file_shareapp:file_download_view', args=[file_id])
        )
        self.assertEqual(response.status_code, 404)


class FileDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='test-pass-123'
        )
        self.client.login(username='tester', password='test-pass-123')
        self.file_obj = File.objects.create(
            user=self.user,
            title='Delete File',
            uploaded_file=sample_file(),
            expiry_date=date.today() + timedelta(days=7),
        )

    def test_delete_removes_file_and_redirects(self):
        response = self.client.get(
            reverse('file_shareapp:file_delete_view', args=[self.file_obj.id])
        )
        self.assertRedirects(response, reverse('file_shareapp:dashboard'))
        self.assertEqual(File.objects.count(), 0)