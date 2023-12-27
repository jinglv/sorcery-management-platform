from enum import Enum
from typing import List, Any

from ninja import Schema


class CaseSuiteIn(Schema):
    """
    测试用例集入参
    """
    name: str
    status: int = 1
    version_number: str
    case_ids: list[int] = None
    describe: str = None


class CaseSuiteSearchIn(Schema):
    """
    测试用例集查询入参
    """
    name: str
    version_number: str
    status: int


class CaseSuiteListOut(Schema):
    """
    测试用例集查询出参
    """
    id: int
    name: str
    version_number: str
    case_ids: list[int]
    case_number: int
    status: int
    describe: str


class CaseStepIn(Schema):
    """
    测试步骤入参
    """
    id: int = None
    test_step: str
    test_data: str = None
    expected_result: str
    remark: str = None
    api_id: int = None


class TestLabel(int, Enum):
    """
    测试用例标签
    """
    usual = 1
    unusual = 2


class TestCaseType(int, Enum):
    """
    测试用例类型
    """
    function = 1
    api = 2


class ImportanceType(int, Enum):
    """
    重要程度类型
    """
    p0 = 1
    p1 = 2
    p3 = 2
    p4 = 2


class PriorityType(int, Enum):
    """
    优先级类型
    """
    high = 1
    mid = 2
    low = 3


class CaseIn(Schema):
    """
    新增测试用例入参
    """
    name: str
    version_number: list[str] = None
    project_id: int
    module_id: int
    test_label: TestLabel
    type: TestCaseType
    importance: ImportanceType
    priority: PriorityType
    precondition: str
    test_steps: List[CaseStepIn]
    remark: str = None


class CaseStepOut(Schema):
    """
    测试步骤出参
    """
    id: int
    test_step: str
    test_data: str
    expected_result: str
    api_id: int
    remark: str


class CaseListOut(Schema):
    """
    查询测试用例出参
    """
    id: int
    name: str
    project_id: int
    project_name: str
    module_id: int
    module_name: str
    version_info: List
    type: int
    test_label: int
    importance: int
    priority: int
    precondition: str
    test_steps: List[CaseStepOut]
    create_time: Any
    update_time: Any


class CaseSearchIn(Schema):
    """
    测试用例查询入参
    """
    name: str
    project_id: int
    module_id: int
    type: int
    test_label: int
    importance: int
    priority: int


class RequirementsType(str, Enum):
    """
    需求类型
    """
    business = "business"
    improve = "improve"
    technical = "technical"


class DemandVersionInfoIn(Schema):
    """
    新增需求信息入参
    """
    name: str
    project_id: int
    version_number: str
    requirements_type: RequirementsType
    requirements: str = None
    requirements_upload_file: list[str] = None
    demand_analysis: str = None
    describe: str = None


class DemandInfoSearchIn(Schema):
    """
    需求信息查询入参
    """
    name: str
    project_id: int
    version_number: str
    requirements_type: str
    create_time: Any = None


class ProjectSchema(Schema):
    """
    项目信息入参
    """
    id: int
    name: str


class DemandInfoListOut(Schema):
    """
    查询需求信息出参
    """
    id: int
    name: str
    project_id: int
    project: ProjectSchema
    version_number: str
    requirements_type: RequirementsType
    requirements: str
    requirements_upload_file: str
    demand_analysis: str
    create_time: Any
    update_time: Any
