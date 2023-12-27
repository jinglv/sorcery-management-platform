from enum import Enum
from typing import Any

from ninja import Schema


class HttpRunnerProjectInfoIn(Schema):
    """
     HttpRunnerProject入参
    """
    project_id: int
    name: str
    describe: str = None
    code: str
    env_code: str


class DebugTalkCodeIn(Schema):
    """
    debugtalk入参代码
    """
    code: str


class HttpRunnerProjectInfoOut(Schema):
    """
    项目列表出参
    """
    id: int
    project_id: int
    project_name: str
    name: str
    describe: str
    code: str
    env_code: str
    create_time: Any
    update_time: Any


class HttpRunnerApiInfoIn(Schema):
    """
    HttpRunner维护接口信息入参
    """
    httprunner_project_id: int
    base_api_id: int
    name: str


class HttpRunnerListOut(Schema):
    """
    HttpRunner接口列表出参
    """
    id: int
    name: str
    httprunner_project_name: str
    status: str
    report_name: str
    create_time: Any


class HttpRunnerSearchIn(Schema):
    """
    HttpRunner搜索条件
    """
    name: str
    httprunner_project_id: int


class Type(str, Enum):
    """
    执行类型
    """
    api = "API"
    case = "TESTCASE"
    suite = "TESTSUITE"


class HttpRunnerApiRunIn(Schema):
    """
    HttpRunner接口执行入参
    """
    httprunner_project_id: int
    api_ids: list
    type: Type
    env_url: str


class infoIn(Schema):
    """
    信息入参
    """
    id: int
    name: str


class HttpRunnerApiResultListOut(Schema):
    """
    HttpRunner接口列表出参
    """
    id: int
    name: str
    type: str
    result: str
    ids: list[infoIn]
    create_time: Any


class HttpRunnerUpdateApiInfoIn(Schema):
    """
    HttpRunner维护接口信息入参
    """
    api_info: dict
    name: str
    pre_processor: str = None
    post_processor: str = None


class TestCaseApiInfoIn(Schema):
    """
    HttpRunner测试用例信息信息入参
    """
    name: str
    api_id: int
    variables: dict = None
    extracts: dict = None
    validates: list = None


class HttpRunnerTestCaseIn(Schema):
    """
    HttpRunner测试用例信息入参
    """
    name: str
    public_variables: dict = None
    httprunner_project_id: int
    test_case_infos: list[TestCaseApiInfoIn]
    pre_processor: str = None
    post_processor: str = None


class HttpRunnerCasesRunIn(Schema):
    """
    HttpRunner接口执行入参
    """
    httprunner_project_id: int
    cases_ids: list[int]
    type: Type
    env_url: str


class TestCaseInfoIn(Schema):
    """
    用例集用例信息入参
    """
    name: str
    case_id: int
    params: dict = None
    variables: dict = None


class HttpRunnerSuiteIn(Schema):
    """
    HttpRunner测试用例集信息入参
    """
    name: str
    public_variables: dict = None
    httprunner_project_id: int
    test_cases: list[TestCaseInfoIn]


class HttpRunnerSuiteRunIn(Schema):
    """
    HttpRunner接口执行入参
    """
    httprunner_project_id: int
    suite_ids: list[int]
    type: Type
    env_url: str
