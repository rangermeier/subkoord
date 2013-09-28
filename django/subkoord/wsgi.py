import os

NEWRELIC_CONF = os.path.join(os.path.dirname(__file__), "newrelic.ini")
if os.path.exists(NEWRELIC_CONF):
    try:
        import newrelic.agent
        newrelic.agent.initialize(NEWRELIC_CONF)
        print "starting with newrelic"
    except ImportError:
        pass


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subkoord.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
