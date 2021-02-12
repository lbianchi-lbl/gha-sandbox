import os
from pathlib import Path
import sys

from ghapi.all import GhApi
from ghapi.actions import context_github

from .actions import get_api
from .models import GitHubContext
from .util import LabelAddTrigger
from .logging_ import get_logger


log = get_logger()

# TODO use owner, repo and token from GitHub Actions runner env
api = get_api()


# github = GitHubContext()
# event = github.event_payload
github = context_github


try:
    _script = sys.argv[1]
except IndexError:
    _script = 'print(api)'
log.display(script=_script)
try:
    log.info('exec()ing script...')
    exec(_script)
except Exception as e:
    log.critical('Could not execute script:')
    log.exception(e)
    log.display(script=_script)
    sys.exit(1)
else:
    log.info('Done')
