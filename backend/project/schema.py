from typing import Any

from ninja import Schema


class ProjectIn(Schema):
    """
    新建项目入参
    """
    name: str
    describe: str
    image: str = None


class ProjectSearchIn(Schema):
    """
    新建项目入参
    """
    name: str


class ProjectListOut(Schema):
    """
    项目列表出参
    """
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
