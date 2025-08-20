import os
import sys

sys.path.insert(0, '/home/arogya/Arogya_Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arogya_Backend.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
