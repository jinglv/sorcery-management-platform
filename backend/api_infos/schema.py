from typing import Any

from ninja import Schema


class HarFileIn(Schema):
    """
    har文件名称
    """
    har_file: str


class InfosIn(Schema):
    """
    接口信息入参
    """
    name: str
    url: str
    method: str
    request_headers: list
    request_params: list
    request_body: dict
    response_body: str


class InfosSearchListIn(Schema):
    """
    查询信息列表入参
    """
    file_name: str


class InfosOut(Schema):
    """
    接口信息查询出参
    """
    id: int
    name: str
    url: str
    method: str
    request_headers: list
    request_params: list
    request_body: dict
    response_body: dict
    create_time: Any


class YapiBaseIn(Schema):
    """
    yapi获取信息入参
    """
    yapi_base_url: str
    yapi_token: str


class YapiIn(Schema):
    """
    yapi获取信息入参
    """
    yapi_base_url: str
    yapi_token: str
    project_id: int


class YapiCategoryApiIn(Schema):
    """
    获取分类下的接口信息入参
    """
    yapi_base_url: str
    yapi_token: str
    category_id: int
    page: int
    size: int


class YapiApiListOut(Schema):
    """
    接口列表查询出参
    """
    project_id: int
    category_id: int
    api_id: int
    api_name: str
    api_path: str


class YapiApiDetailsIn(Schema):
    """
    获取分类下的接口信息入参
    """
    yapi_base_url: str
    yapi_token: str
    api_id: int
