import os
import tempfile

# Set dummy environment variables before importing the real settings so the
# required environment variable lookups in settings.py do not trip during tests.
os.environ.setdefault('DJANGO_SECRET_KEY', 'test-secret-key')
os.environ.setdefault('POSTGRES_DB', 'test_db')
os.environ.setdefault('POSTGRES_USER', 'test_user')
os.environ.setdefault('POSTGRES_PASSWORD', 'test-password')
os.environ.setdefault('POSTGRES_HOST', 'localhost')
os.environ.setdefault('AZURE_ACCOUNT_NAME', 'test-account')
os.environ.setdefault('AZURE_ACCOUNT_KEY', 'test-account-key')

from Nimubus.settings import *  # noqa: E402,F401,F403

# --- Test overrides --------------------------------------------------------

# Use an in-memory SQLite database instead of PostgreSQL so tests run without
# requiring a running Postgres instance.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Speed up test runs by using Django's fast (but insecure) password hasher.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Store uploaded files on the local filesystem instead of Azure Blob Storage so
# tests do not require external cloud services.
MEDIA_ROOT = tempfile.mkdtemp(prefix='nimbus-test-media-')
STORAGES['default'] = {
    'BACKEND': 'django.core.files.storage.FileSystemStorage',
    'OPTIONS': {},
}
