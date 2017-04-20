import os
import dj_database_url
from memcacheify import memcacheify

from settings import *

# No debug
DEBUG = False
TEMPLATE_DEBUG = False

# Heroku hosted database & cache
DATABASES['default'] = dj_database_url.config()
CACHES = memcacheify(timeout=60)  # cache for max one minute

# Sendgrid email
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']

# SSL
SSLIFY_DISABLE = False
SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}',) # for cloudflare
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # for heroku
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Allowed host headers
ALLOWED_HOSTS = ['stories-of-solidarity.herokuapp.com', 'app.storiesofsolidarity.org']
CORS_ORIGIN_WHITELIST = [
    'storiesofsolidarity.org', 'www.storiesofsolidarity.org',
    'storiesofsolidarity.github.io', 'localhost:9000'
]

# Twilio
#bug w/ django-twilio on heroku, avoid temporarily
DJANGO_TWILIO_FORGERY_PROTECTION = False

# Share session cookies with frontend
# SESSION_COOKIE_DOMAIN = '.storiesofsolidarity.org'

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
MEDIA_URL = 'https://storiesofsolidarity.s3-website-us-west-2.amazonaws.com/'

# us-data repository
ZIPCODE_LOOKUP_URL = 'https://raw.githubusercontent.com/storiesofsolidarity/us-data/gh-pages/geography/zipcodes/all/%s.geo.json'

import raven

RAVEN_CONFIG = {
    'dsn': 'https://32e87c2362874c5aae24477af20b5fe0:ef56f3206cef406fa063d4934e3a883a@app.getsentry.com/54639',
}
