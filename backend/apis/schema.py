from enum import Enum
from typing import Any

from ninja import Schema


class Method(str, Enum):
    """
    请求方法
    """
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"


class ParamsType(str, Enum):
    """
    参数类型
    """
    params = "params"
    form = "form"
    json = "json"


class AssertType(str, Enum):
    """
    断言类型
    """
    contains = "contains"
    equal = "equal"


class ApiInfoAssertIn(Schema):
    """
    接口断言入参
    """
    name: str
    assert_type: AssertType
    assert_extract: str
    expect_text: str


class ApiInfoIn(Schema):
    """
    接口信息入参
    """
    name: str
    module_id: int
    api_path: str
    method: Method
    header: list
    params_type: ParamsType
    params_body: Any
    response: str
    assert_list: list[ApiInfoAssertIn] = None
    extract_list: list = None
    extract_result_list: list = None


class ApiDebugIn(Schema):
    """
    接口调试入参
    """
    url: str
    method: str
    header: list
    params_type: str
    params_body: Any


class ApiAssertIn(Schema):
    """
    接口断言入参
    """
    response: dict
    assert_type: AssertType
    assert_extract: str
    expect_text: str


class ModuleSchema(Schema):
    """
    模块信息入参
    """
    id: int
    name: str


class ApiInfoForModuleOut(Schema):
    """
    模块下接口信息的出参
    """
    id: int
    name: str
    module_id: int
    api_path: str
    method: str
    module: ModuleSchema = None  # 关联模块
    create_time: Any
    update_time: Any


class CheckExtractIn(Schema):
    """
    检查器入参
    """
    response: dict
    extractList: list


class ExtractOut(Schema):
    """
    提取器变量返回
    """
    id: int
    name: str
    extract: str
    value: str
    apis_id: str
    create_time: Any
    update_time: Any


class ExtractSearchIn(Schema):
    """
    提取器搜索条件
    """
    name: str
    project_id: int


class ApiSearchIn(Schema):
    """
    接口信息查询入参
    """
    name: str
    api_path: str
    method: str
    create_time: Any = None
