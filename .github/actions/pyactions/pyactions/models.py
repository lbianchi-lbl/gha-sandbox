from pathlib import Path
import typing as t

from pydantic import BaseModel, BaseSettings, Field, Extra


class GitHubContext(BaseSettings):
    action: str
    workflow: str
    event_name: str
    event_path: t.Optional[Path] = None
    sha: str
    action_ref: str
    action_repository: str
    actor: str
    api_url: str
    base_ref: str = None

    class Config:
        env_prefix = 'GITHUB_'
        case_sensitive = False
        extra = Extra.ignore


