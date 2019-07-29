import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/assets/'

# Extra places to collect and find static files
# STATICFILES_DIRS = (os.path.join(BASE_DIR, '/assets/'))