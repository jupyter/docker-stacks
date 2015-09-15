# Copyright (c) Jupyter Development Team.
from jupyter_core.paths import jupyter_data_dir
import subprocess
import os

PEM_FILE = os.path.join(jupyter_data_dir(), 'notebook.pem')

c = get_config()
c.NotebookApp.ip = os.getenv('INTERFACE', '') or '*'
c.NotebookApp.port = int(os.getenv('NB_PORT', '') or 8888)
c.NotebookApp.open_browser = False

# Set a certificate if USE_HTTPS is set to any value
if 'USE_HTTPS' in os.environ:
    if not os.path.isfile(PEM_FILE):
        # Generate a certificate if one doesn't exist on disk
        subprocess.check_call(['openssl', 'req', '-new', 
            '-newkey', 'rsa:2048', '-days', '365', '-nodes', '-x509',
            '-subj', '/C=XX/ST=XX/L=XX/O=generated/CN=generated',
            '-keyout', PEM_FILE, '-out', PEM_FILE])
    c.NotebookApp.certfile = PEM_FILE

# Set a password if PASSWORD is set
if 'PASSWORD' in os.environ:
    from IPython.lib import passwd
    c.NotebookApp.password = passwd(os.environ['PASSWORD'])
    del os.environ['PASSWORD']