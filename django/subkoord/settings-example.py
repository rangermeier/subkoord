# Django settings for subkoord project.
import os
import sys
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Django 1.4
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/.../media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'


SITE_URL = 'http://domain.com'

ALLOWED_HOSTS = ["domain.com"]

# Static File configuration
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static/'),
)

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'subkoord.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

WSGI_APPLICATION = 'subkoord.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'south',
    'crispy_forms',
    'tinymce',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.messages',
    'event',
    'users',
    'wiki',
    'newsletter',
    'attachment',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_URL = 'http://127.0.0.1:8000'

# when to start bragging about open tasks (hours)
EVENT_REMINDER_WINDOW = 48
# Pause between two reminders (hours)
EVENT_REMINDER_PAUSE = 24
# Subject for reminder e-mails
EVENT_REMINDER_SUBJECT = "there's something to do"
# List of e-mail addresses to send reminder to
EVENT_REMINDER_ADDRESSBOOK = ["mailinglist@example.com",]
# From:
EVENT_REMINDER_FROM = "bar@example.com"
# Timezone (a tzinfo subclass) used in ical-export
from pytz import timezone
EVENT_TIMEZONE = timezone(TIME_ZONE)

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Directory for DB dumps
BACKUP_DIR = '/home/.../private/backup/subkoord'

# the newsletter should be invoked regularly by a cronjob
# on each run it will send emails according to NEWSLETTER_QUOTA
NEWSLETTER_QUOTA = 28

# Mailing with less subscribers are offered for preview mailing
# after sending a preview newsletter the message won't be locked
NEWSLETTER_PREVIEW_LIST = 5

# Host and credentials for error-mailbox (should be the "technical"-From address
# uses POP3 over SSL at Port 995
NEWSLETTER_ERROR_MAILBOX = 'mail.newsletter.yourhost.org'
NEWSLETTER_ERROR_USER = 'catch-all@newsletter.yourhost.org'
NEWSLETTER_ERROR_PASS = 'password'

# Filebrowser Settings
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_DIRECTORY = ""

# Grapelli
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
GRAPPELLI_ADMIN_TITLE = "Admin"

# TinyMCE
TINYMCE_JS_URL = STATIC_URL+'/tiny_mce/tiny_mce_src.js'
TINYMCE_JS_ROOT = os.path.join(PROJECT_ROOT, 'static/tiny_mce')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste",
    'theme': "advanced",
    'mode' : "textareas",
    'theme_advanced_buttons1' : "cut,copy,paste,pastetext,pasteword,|,undo,redo,|,link,unlink,anchor,image,charmap,|,code,cleanup,removeformat,visualaid",
    'theme_advanced_buttons2' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull|,bullist,numlist,|,outdent,indent,blockquote,|,hr",
    'theme_advanced_buttons3' : "tablecontrols",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_resizing' : 'true',
}
TINYMCE_COMPRESSOR = False
