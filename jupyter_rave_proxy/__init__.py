import getpass
import os
import pathlib
import shutil
import subprocess
import tempfile
import pwd
from textwrap import dedent
from urllib.parse import urlparse, urlunparse

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'rave.png'
    )

def rewrite_netloc(response, request):
    '''
       In some circumstances, rstudio-server appends a port to the URL while
       setting Location in the header. We rewrite the response to use the host
       in the request.
    '''
    for header, v in response.headers.get_all():
        if header == "Location":
            u = urlparse(v)
            if u.netloc != request.host:
                response.headers[header] = urlunparse(u._replace(netloc=request.host))

def get_system_user():
    try:
        user = pwd.getpwuid(os.getuid())[0]
    except:
        user = os.environ.get('NB_USER', getpass.getuser())
    return(user)

def setup_rave():
    def _get_env(port):
        # Detect various environment variables rsession requires to run
        # Via rstudio's src/cpp/core/r_util/REnvironmentPosix.cpp
        cmd = ['R', '--slave', '--vanilla', '-e',
                'cat(paste(R.home("home"),R.home("share"),R.home("include"),R.home("doc"),getRversion(),sep=":"))']

        r_output = subprocess.check_output(cmd)
        R_HOME, R_SHARE_DIR, R_INCLUDE_DIR, R_DOC_DIR, version = \
            r_output.decode().split(':')

        return {
            'R_DOC_DIR': R_DOC_DIR,
            'R_HOME': R_HOME,
            'R_INCLUDE_DIR': R_INCLUDE_DIR,
            'R_SHARE_DIR': R_SHARE_DIR,
            'RSTUDIO_DEFAULT_R_VERSION_HOME': R_HOME,
            'RSTUDIO_DEFAULT_R_VERSION': version,
        }

    def _get_cmd(port):
        return [
            'R',
            '-e',
            f'rave::start_rave2(port={ port }, launch.browser = FALSE, as_job = FALSE)'
        ]

    def _get_timeout(default=150000):
        try:
            return float(os.getenv('RSESSION_TIMEOUT', default))
        except Exception:
            return default

    return {
        'command': _get_cmd,
        'timeout': _get_timeout(),
        'environment': _get_env,
        'rewrite_response': rewrite_netloc,
        'launcher_entry': {
            'title': 'RAVE-iEEG',
            'icon_path': get_icon_path()
        }
    }
