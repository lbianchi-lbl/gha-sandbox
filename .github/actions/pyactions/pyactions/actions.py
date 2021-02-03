import contextlib
import json
import os
from pathlib import Path
import typing as t

from ghapi.all import GhApi


class Logger:
    "Pseudo-logging.Logger compatible with GitHub Actions workflow commands output format"

    def debug(self, msg):
        print(f"::debug::{msg}")

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        print(f"::warning::{msg}")

    def error(self, msg):
        print(f"::error::{msg}")

    def critical(self, msg):
        self.error(f"CRITICAL: {msg}")

    @contextlib.contextmanager
    def group(self, title):
        print(f"::group::{title}")
        yield
        print(f"::endgroup::")

    def exception(self, e):
        with self.group(str(e)):
            self.info(e)

    def display(self, title, obj):
        with self.group(title):
            self.info(obj)


def get_github_env(name: str, fallback="", prefix: str = 'GITHUB_'):
    return os.environ.get(f"{prefix}{name.upper()}", fallback)


class GitHubContext:
    "Info about environment in object form. Like the `github` context accessible to workflows."

    @property
    def action(self) -> str:
        return get_github_env('action')

    @property
    def workflow(self) -> str:
        return get_github_env('workflow')

    @property
    def event_name(self) -> str:
        return get_github_env('event_name')

    @property
    def event_path(self) -> Path:
        return Path(get_github_env('event_path'))

    @property
    def event_payload(self) -> t.Mapping:
        if not self.event_path.is_file():
            return {}
        with self.event_path.open() as f:
            return json.load(f)

    @property
    def sha(self) -> str:
        return get_github_env('sha')


def get_api():
    owner, repo = get_github_env('repository').split('/')
    token = get_github_env('token')
    return GhApi(owner=owner, repo=repo, token=token)
