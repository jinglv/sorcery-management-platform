from typing import Any

from ninja import Schema


class EnvIn(Schema):
    """
    环境入参
    """
    name: str
    project_id: int
    env: str
    browser: str
    protocol: str
    base_url: str


class EnvSearchIn(Schema):
    """
    环境入参
    """
    name: str
    project_id: int
    env: str
    browser: str
    protocol: str
    base_url: str


class EnvListOut(Schema):
    """
    环境列表出参
    """
    id: int
    name: str
    project_id: int
    project_name: str
    env: str
    browser: str
    base_url: str
    protocol: str
    create_time: Any
    update_time: Any
