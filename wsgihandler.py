#!/srv/www/gyuris.hu/op.gyuris.hu/.venv/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/srv/www/gyuris.hu/op.gyuris.hu/")
sys.path.insert(0,"/srv/www/gyuris.hu/op.gyuris.hu/.venv/lib/python3.11/site-packages")
 
from app import app as application
#application.secret_key = ‘fhkjdskjgf(anything)’
