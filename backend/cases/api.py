# Create your views here.
import json
from typing import List

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from apis.models import ApiInfo
from backend.common import response, Error, model_to_dict
from backend.pagination import CustomPagination
from cases.models import CasesSuite, VersionInfo, TestStep, TestCase
from cases.schema import CaseSuiteIn, CaseIn, CaseListOut, CaseSearchIn, DemandVersionInfoIn, DemandInfoListOut, \
    DemandInfoSearchIn, CaseSuiteSearchIn, CaseSuiteListOut
from modules.models import Module
from project.models import Project

router = Router(tags=["cases"])


@router.post("/suite/create")
@transaction.atomic
def create_case_suite(request, data: CaseSuiteIn):
    """
    创建测试用例集
    """
    # 查询测试用例集是否存在
    caseSuite = CasesSuite.objects.filter(name=data.name).filter(version_number=data.version_number)
    if len(caseSuite) > 0:
        return response(error=Error.CASE_SUITE_NAME_EXIST)
    result = CasesSuite.objects.create(**data.dict())
    return response(item=model_to_dict(result))


@router.post("/suites", response=List[CaseSuiteListOut])
@paginate(CustomPagination)
def test_suite_list(request, data: CaseSuiteSearchIn):
    # 构造多条件查询条件
    query = Q() & Q(is_delete=False)
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.version_number:
        query &= Q(version_number=data.version_number)
    if data.status:
        query &= Q(status=data.status)
    test_suites = CasesSuite.objects.filter(query).all()
    suites = []
    for s in test_suites:
        case_ids = json.loads(s.case_ids)
        suite = {
            'id': s.id,
            'name': s.name,
            'version_number': s.version_number,
            'case_ids': case_ids,
            'case_number': len(case_ids),
            'status': s.status,
            'describe': s.describe
        }
        suites.append(suite)
    return suites


@router.get("/suite/{case_suite_id}")
@transaction.atomic
def case_suite_detail(request, case_suite_id: int):
    """
    测试用例集详情
    """
    case_suite = get_object_or_404(CasesSuite, id=case_suite_id)
    case_ids = json.loads(case_suite.case_ids)
    test_cases = []
    for id in case_ids:
        test_case = get_object_or_404(TestCase, id=id)
        module = get_object_or_404(Module, id=test_case.module_id, is_delete=False)
        project = get_object_or_404(Project, id=test_case.project_id, is_delete=False)
        case = {
            'id': test_case.id,
            'name': test_case.name,
            'project_id': test_case.project_id,
            'project_name': project.name,
            'module_id': test_case.module_id,
            'module_name': module.name,
            'version_number': json.loads(test_case.version_number.replace('\'', '\"')),
            'type': test_case.type,
            'test_label': test_case.test_label,
            'importance': test_case.importance,
            'priority': test_case.priority,
            'precondition': test_case.precondition,
            'remark': test_case.remark,
            'create_time': test_case.create_time,
            'update_time': test_case.update_time
        }
        test_cases.append(case)
    versions = []
    version = get_object_or_404(VersionInfo, version_number=case_suite.version_number)
    version_for_project = get_object_or_404(Project, id=version.project_id, is_delete=False)
    version_info = {
        "name": version.name,
        "version_number": version.version_number,
        "project_id": version.project_id,
        "project_name": version_for_project.name,
        "requirements_type": version.requirements_type,
        "describe": version.describe,
        "create_time": version.create_time
    }
    versions.append(version_info)
    result = {
        'id': case_suite.id,
        'name': case_suite.name,
        'version_info': versions,
        'test_cases': test_cases,
        'status': int(case_suite.status),
        'describe': case_suite.describe,
        'create_time': case_suite.create_time,
        'update_time': case_suite.update_time
    }
    return response(item=result)


@router.put("/suite/{case_suite_id}")
@transaction.atomic
def case_suite_update(request, case_suite_id: int, data: CaseSuiteIn):
    """
    模块删除
    """
    case_suite = get_object_or_404(CasesSuite, id=case_suite_id)
    for attr, value in data.dict().items():
        setattr(case_suite, attr, value)
    case_suite.save()
    return response()


@router.delete("/suite/{case_suite_id}")
@transaction.atomic
def case_suite_delete(request, case_suite_id: int):
    """
    模块删除
    """
    case_suite = get_object_or_404(CasesSuite, id=case_suite_id)
    case_suite.delete()
    return response()


@router.post("/create")
@transaction.atomic
def create_test_case(request, data: CaseIn):
    """
    新增测试用例
    """
    # 存储测试步骤
    for step in data.test_steps:
        TestStep.objects.create(
            name=data.name,
            test_step=step.test_step,
            test_data=step.test_data,
            expected_result=step.expected_result,
            remark=step.remark,
            api_id=step.api_id
        )
    # 查询测试用例步骤，获取id存储
    test_step_ids = []
    test_steps = TestStep.objects.filter(name=data.name)
    for step in test_steps:
        test_step_ids.append(step.id)
    # for item in data.test_steps:
    #     test_step = get_object_or_404(TestStep, test_step=item.test_step)
    #     test_step_ids.append(test_step.id)
    # 查询项目模块是否存在
    get_object_or_404(Module, id=data.module_id)
    # 保存测试用例
    TestCase.objects.create(
        module_id=data.module_id,
        project_id=data.project_id,
        version_number=data.version_number,
        name=data.name,
        type=data.type,
        test_label=data.test_label,
        importance=data.importance,
        priority=data.priority,
        precondition=data.precondition,
        remark=data.remark,
        test_steps=test_step_ids
    )
    return response()


@router.post("/list", response=List[CaseListOut])
@paginate(CustomPagination)
def test_case_list(request, data: CaseSearchIn):
    """
    测试用例查询列表
    """
    # 构造多条件查询条件
    query = Q() & Q(is_delete=False)
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.project_id:
        query &= Q(project_id=data.project_id)
    if data.module_id:
        query &= Q(module_id=data.module_id)
    if data.type:
        query &= Q(type=data.type)
    if data.test_label:
        query &= Q(test_label=data.test_label)
    if data.importance:
        query &= Q(importance=data.importance)
    if data.priority:
        query &= Q(priority=data.priority)
    test_cases = TestCase.objects.filter(query).all()
    cases = []
    for test_case in test_cases:
        versions = []
        version_numbers = json.loads(test_case.version_number.replace('\'', '\"'))
        for version in version_numbers:
            query_version_info = get_object_or_404(VersionInfo, version_number=version)
            version_info = {
                'id': query_version_info.id,
                'version_number': query_version_info.version_number,
                'requirements': query_version_info.requirements,
                'describe': query_version_info.describe
            }
            versions.append(version_info)
        test_steps = []
        for test_step_ids in json.loads(test_case.test_steps):
            test_step = get_object_or_404(TestStep, id=test_step_ids)
            test_steps.append({
                'id': test_step.id,
                'test_step': test_step.test_step,
                'test_data': test_step.test_data,
                'expected_result': test_step.expected_result,
                'remark': test_step.remark,
                'api_id': test_step.api_id
            })
        module = get_object_or_404(Module, id=test_case.module_id, is_delete=False)
        project = get_object_or_404(Project, id=test_case.project_id, is_delete=False)
        case = {
            'id': test_case.id,
            'name': test_case.name,
            'project_id': test_case.project_id,
            'project_name': project.name,
            'module_id': test_case.module_id,
            'module_name': module.name,
            'version_info': versions,
            'type': test_case.type,
            'test_label': test_case.test_label,
            'importance': test_case.importance,
            'priority': test_case.priority,
            'precondition': test_case.precondition,
            'test_steps': test_steps,
            'remark': test_case.remark,
            'create_time': test_case.create_time,
            'update_time': test_case.update_time
        }
        cases.append(case)
    return cases


@router.get("/detail/{test_case_id}")
def test_case_detail(request, test_case_id: int):
    """
    测试用例详情
    """
    try:
        test_case = TestCase.objects.get(id=test_case_id)
    except test_case.DoesNotExist:
        return response(error=Error.TEST_CASE_IS_NULL)
    versions = []
    version_numbers = json.loads(test_case.version_number.replace('\'', '\"'))
    for version in version_numbers:
        query_version_info = get_object_or_404(VersionInfo, version_number=version)
        project = get_object_or_404(Project, id=query_version_info.project_id, is_delete=False)
        version_info = {
            'id': query_version_info.id,
            'name': query_version_info.name,
            'project_name': project.name,
            'version_number': query_version_info.version_number,
            'requirements_type': query_version_info.requirements_type,
            'requirements': query_version_info.requirements,
            'describe': query_version_info.describe
        }
        versions.append(version_info)
    test_steps = []
    for test_step_ids in json.loads(test_case.test_steps):
        test_step = get_object_or_404(TestStep, id=test_step_ids)
        if test_step.api_id != 0:
            api_info = get_object_or_404(ApiInfo, pk=test_step.api_id, is_delete=False)
            api_name = api_info.name
        else:
            api_name = ''
        test_steps.append({
            'id': test_step.id,
            'test_step': test_step.test_step,
            'test_data': test_step.test_data,
            'expected_result': test_step.expected_result,
            'remark': test_step.remark,
            'api_id': test_step.api_id,
            'api_name': api_name
        })
    module = get_object_or_404(Module, id=test_case.module_id, is_delete=False)
    project = get_object_or_404(Project, id=test_case.project_id, is_delete=False)
    result = {
        'name': test_case.name,
        'project_id': test_case.project_id,
        'project_name': project.name,
        'module_id': test_case.module_id,
        'module_name': module.name,
        'version_number': test_case.version_number,
        'version_info': versions,
        'type': test_case.type,
        'test_label': test_case.test_label,
        'importance': test_case.importance,
        'priority': test_case.priority,
        'precondition': test_case.precondition,
        'test_steps': test_steps,
        'remark': test_case.remark,
        'create_time': test_case.create_time,
        'update_time': test_case.update_time
    }
    return response(item=result)


@router.put("/update/{test_case_id}")
@transaction.atomic
def update_test_case(request, test_case_id: int, data: CaseIn):
    """
    更新测试用例
    """
    # 查询用例是否存在
    get_object_or_404(TestStep, pk=test_case_id)
    # 测试步骤更新保存
    for step in data.test_steps:
        test_step_info = TestStep.objects.filter(pk=step.id)
        # test_step_info = get_object_or_404(TestStep, test_step=step.test_step)
        if len(test_step_info) > 0:
            TestStep.objects.filter(pk=step.id).update(
                name=data.name,
                test_step=step.test_step,
                test_data=step.test_data,
                expected_result=step.expected_result,
                remark=step.remark,
                api_id=step.api_id
            )
        else:
            TestStep.objects.create(
                name=data.name,
                test_step=step.test_step,
                test_data=step.test_data,
                expected_result=step.expected_result,
                remark=step.remark,
                api_id=step.api_id
            )
    # 查询测试用例步骤，获取id存储
    test_step_ids = []
    test_steps = TestStep.objects.filter(name=data.name)
    for step in test_steps:
        test_step_ids.append(step.id)
    # 查询项目模块是否存在
    get_object_or_404(Module, id=data.module_id)
    # 更新测试用例
    TestCase.objects.filter(pk=test_case_id).update(
        module_id=data.module_id,
        project_id=data.project_id,
        version_number=data.version_number,
        name=data.name,
        type=data.type,
        test_label=data.test_label,
        importance=data.importance,
        priority=data.priority,
        precondition=data.precondition,
        remark=data.remark,
        test_steps=test_step_ids
    )
    return response()


@router.delete("/delete/{test_case_id}")
@transaction.atomic
def test_case_delete(request, test_case_id: int):
    """
    删除测试用例
    """
    test_case = get_object_or_404(TestCase, id=test_case_id)
    test_case.is_delete = True
    test_case.save()
    return response()


@router.post("/demand/create")
@transaction.atomic
def create_demand(request, data: DemandVersionInfoIn):
    """
    创建需求信息
    """
    get_object_or_404(Project, id=data.project_id)
    # 查询测试用例集是否存在
    versionInfo = VersionInfo.objects.filter(name=data.name)
    if len(versionInfo) > 0:
        return response(error=Error.DEMAND_INFO_NAME_EXIST)
    result = VersionInfo.objects.create(**data.dict())
    return response(item=model_to_dict(result))


@router.get("/demand/detail/{demand_id}")
def detail_demand(request, demand_id: int):
    """
    需求详情
    """
    try:
        demand = VersionInfo.objects.get(id=demand_id)
    except demand.DoesNotExist:
        return response(error=Error.DEMAND_INFO_IS_NULL)
    if demand.is_delete is True:
        return response(error=Error.DEMAND_IS_DELETE)
    project_info = get_object_or_404(Project, id=demand.project_id)
    result = {
        "name": demand.name,
        "version_number": demand.version_number,
        "project_id": demand.project_id,
        "project_name": project_info.name,
        "requirements_type": demand.requirements_type,
        "requirements": demand.requirements,
        "requirements_upload_file": demand.requirements_upload_file,
        "demand_analysis": demand.demand_analysis,
        "describe": demand.describe,
        "create_time": demand.create_time
    }
    return response(item=result)


@router.post("/demand/list", response=List[DemandInfoListOut])
@paginate(CustomPagination)
def demand_list(request, data: DemandInfoSearchIn):
    """
    需求查询列表
    """
    # 构造多条件查询条件
    query = Q() & Q(is_delete=False)
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.version_number:
        query &= Q(version_number=data.version_number)
    if data.requirements_type:
        query &= Q(requirements_type=data.requirements_type)
    return VersionInfo.objects.filter(query).all()


@router.put("/demand/update/{demand_id}")
@transaction.atomic
def update_demand(request, demand_id: int, data: DemandVersionInfoIn):
    """
    更新需求
    """
    demand = get_object_or_404(VersionInfo, id=demand_id)
    for attr, value in data.dict().items():
        setattr(demand, attr, value)
    demand.save()
    return response()


@router.delete("/demand/delete/{demand_id}")
@transaction.atomic
def delete_demand(request, demand_id: int):
    """
    删除需求
    """
    demand = get_object_or_404(VersionInfo, id=demand_id)
    demand.is_delete = True
    demand.save()
    return response()
