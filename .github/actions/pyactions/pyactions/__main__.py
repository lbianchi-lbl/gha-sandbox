import os
from pathlib import Path
import sys

from ghapi.all import GhApi
from ghapi.actions import context_github

from .actions import Logger, get_api
from .models import GitHubContext


_log = Logger()


# TODO use owner, repo and token from GitHub Actions runner env
api = get_api()


# github = GitHubContext()
# event = github.event_payload
github = context_github


try:
    _script = sys.argv[1]
except IndexError:
    _script = 'print(api)'
_log.display("Script", _script)
try:
    _log.info('exec()ing script...')
    exec(_script)
except Exception as e:
    _log.critical('Could not execute script:')
    _log.exception(e)
    _log.display("Script", _script)
    sys.exit(1)
else:
    _log.info('Done')
