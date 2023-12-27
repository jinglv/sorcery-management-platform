# Create your views here.
import json
from typing import List

import jmespath
import requests
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from apis.models import ApiInfo, ApiExtract, ApiAssert
from apis.schema import ApiInfoIn, ApiDebugIn, ApiAssertIn, CheckExtractIn, ApiInfoForModuleOut, ExtractOut, \
    ExtractSearchIn, ApiSearchIn
from backend.common import response, Error, model_to_dict
from backend.pagination import CustomPagination
from modules.models import Module
from .tasks import add

router = Router(tags=["apis"])


@router.post("/create")
@transaction.atomic
def create_apis_info(request, data: ApiInfoIn):
    """
    创建接口信息
    """
    # 判断项目模块是否存在
    module = get_object_or_404(Module, id=data.module_id)
    api_info = ApiInfo.objects.create(
        name=data.name,
        module_id=data.module_id,
        api_path=data.api_path,
        method=data.method,
        header=data.header,
        params_type=data.params_type,
        params_body=data.params_body,
        response=data.response
    )
    # 查询保存最新数据
    info = ApiInfo.objects.filter(name=data.name).reverse()[0]
    # 断言信息保存
    for assert_info in data.assert_list:
        if assert_info.assert_extract == "" or assert_info.expect_text == "":
            continue
        # 查询接口下的的断言信息
        assert_obj = ApiAssert.objects.filter(api_id=info.id, name=assert_info.name)
        if len(assert_obj) > 0:
            ApiAssert.objects.filter(name=assert_info.name).update(assert_extract=assert_info.assert_extract,
                                                                   assert_type=assert_info.assert_type,
                                                                   expect_text=assert_info.expect_text)
        else:
            ApiAssert.objects.create(
                api_id=info.id,
                name=assert_info.name,
                assert_extract=assert_info.assert_extract,
                assert_type=assert_info.assert_type,
                expect_text=assert_info.expect_text
            )
    # 提取器信息保存
    for extract in data.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        # 查询项目下的提取器
        extract_obj = ApiExtract.objects.filter(apis_id=info.id, name=extract["name"])
        for extract_result in data.extract_result_list:
            extract_name = extract['name']
            if extract_name == extract_result["name"]:
                if len(extract_obj) > 0:
                    ApiExtract.objects.filter(name=extract_name).update(extract=extract["value"],
                                                                        value=extract_result["value"])
                else:
                    ApiExtract.objects.create(
                        project_id=module.project_id,
                        apis_id=api_info.id,
                        name=extract["name"],
                        extract=extract["value"],
                        value=extract_result["value"]
                    )
    return response(item=api_info)


@router.post("/debug")
def debug_apis(request, data: ApiDebugIn):
    """
    接口调试
    """
    # 获取传入的参数
    url = data.url
    method = data.method
    # 处理接收的header
    headers = dict
    if len(data.header) == 0:
        headers = {}
    else:
        headers = {item["name"]: item["value"] for item in data.header}
    params_type = data.params_type
    if params_type != 'json':
        if len(data.params_body) == 0:
            params_body = json.dumps({})
        else:
            params = json.loads(data.params_body)
            params_body = {item["name"]: item["value"] for item in params}
    else:
        params_body = json.loads(data.params_body)

    resp = ''
    if method == "get":
        try:
            resp = requests.get(url, headers=headers, params=params_body).text
        except requests.exceptions.MissingSchema:
            return response(error=Error.CASE_URL_PATH_ERROR)

    if method == "post":
        try:
            if params_type == "form":
                resp = requests.post(url, headers=headers, data=params_body).text
            elif params_type == "json":
                resp = requests.post(url, headers=headers, json=params_body).text
            else:
                return response(error=Error.API_PARAMS_ERROR)
        except requests.exceptions.MissingSchema:
            return response(error=Error.CASE_URL_PATH_ERROR)

    if method == "put":
        try:
            if params_type == "form":
                resp = requests.put(url, headers=headers, data=params_body).text
            elif params_type == "json":
                resp = requests.put(url, headers=headers, json=params_body).text
            else:
                return response(error=Error.API_PARAMS_ERROR)
        except requests.exceptions.MissingSchema:
            return response(error=Error.CASE_URL_PATH_ERROR)

    if method == "delete":
        try:
            if params_type == "form":
                resp = requests.delete(url, headers=headers, data=params_body).text
            elif params_type == "json":
                resp = requests.delete(url, headers=headers, json=params_body).text
            else:
                return response(error=Error.API_PARAMS_ERROR)
        except requests.exceptions.MissingSchema:
            return response(error=Error.CASE_URL_PATH_ERROR)
    return response(item={"response": resp})


@router.post("/assert")
def assert_apis(request, data: ApiAssertIn):
    """
    测试接口断言
    """
    resp = data.response
    assert_type = data.assert_type
    expect_text = data.expect_text
    assert_extract = data.assert_extract
    result = jmespath.search(assert_extract, resp)
    if result is None:
        return response(error={"10058": f"断言提取器错误: {assert_extract}"})

    if assert_type == "contains":
        if expect_text in result:
            return response()
        else:
            return response(success=False)
    elif assert_type == "equal":
        if expect_text == result:
            return response()
        else:
            return response(success=False)


@router.post("/extract")
def check_extract(request, data: CheckExtractIn):
    """
    检查提取器
    """
    resp = data.response
    extracts = data.extractList
    results = []
    for extract in extracts:
        extract_name = extract["name"]
        extract_value = extract["value"]
        if extract_name == "" or extract_value == "":
            continue
        result = jmespath.search(extract_value, resp)
        if result is None:
            return response(error={"10057": f"提取器错误: {extract_value}"})
        results.append({
            "name": extract["name"],
            "value": result
        })
    return response(item=results)


@router.get("/{apis_id}")
def detail_apis(request, apis_id: int):
    """
    接口信息详情
    """
    apis_info = get_object_or_404(ApiInfo, id=apis_id)
    if apis_info.is_delete is True:
        return response(error=Error.API_IS_DELETE)
    test_extract = ApiExtract.objects.filter(apis_id=apis_info.id)
    extracts = []
    for extract in test_extract:
        extracts.append({
            "name": extract.name,
            "value": extract.extract
        })
    apis_info_dict = model_to_dict(apis_info)
    apis_info_dict["module_id"] = apis_info_dict["module"]
    apis_info_dict["extract_list"] = extracts
    test_assert = ApiAssert.objects.filter(api_id=apis_info.id)
    assert_list = []
    for assert_info in test_assert:
        assert_list.append({
            "name": assert_info.name,
            "assert_type": assert_info.assert_type,
            "assert_extract": assert_info.assert_extract,
            "expect_text": assert_info.expect_text
        })
    apis_info_dict["assert_list"] = assert_list
    return response(item=apis_info_dict)


@router.put("/{apis_id}")
@transaction.atomic
def update_apis(request, apis_id: int, data: ApiInfoIn):
    """
    更新接口
    """
    # 判断项目模块是否存在
    apis_info = get_object_or_404(ApiInfo, id=apis_id)
    for attr, value in data.dict().items():
        setattr(apis_info, attr, value)
    apis_info.save()

    # 断言信息保存
    for assert_info in data.assert_list:
        if assert_info.assert_extract == "" or assert_info.expect_text == "":
            continue
        # 查询接口下的的断言信息
        assert_obj = ApiAssert.objects.filter(api_id=apis_info.id, name=assert_info.name)
        if len(assert_obj) > 0:
            # 如果存在则更新
            ApiAssert.objects.filter(name=assert_info.name).update(assert_extract=assert_info.assert_extract,
                                                                   assert_type=assert_info.assert_type,
                                                                   expect_text=assert_info.expect_text)
        else:
            # 不存在则创建
            ApiAssert.objects.create(
                api_id=apis_info.id,
                name=assert_info.name,
                assert_extract=assert_info.assert_extract,
                assert_type=assert_info.assert_type,
                expect_text=assert_info.expect_text
            )

    module = get_object_or_404(Module, id=data.module_id)
    for extract in data.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        extract_obj = ApiExtract.objects.filter(apis_id=apis_info.id, name=extract["name"])
        for extract_result in data.extract_result_list:
            extract_name = extract['name']
            if extract_name == extract_result["name"]:
                if len(extract_obj) > 0:
                    ApiExtract.objects.filter(name=extract_name).update(extract=extract["value"],
                                                                        value=extract_result["value"])
                else:
                    ApiExtract.objects.create(
                        project_id=module.project_id,
                        apis_id=apis_info.id,
                        name=extract["name"],
                        extract=extract["value"],
                        value=extract_result["value"]
                    )
    return response()


@router.delete("/{apis_id}")
@transaction.atomic
def delete_apis(request, apis_id: int):
    """
    删除接口信息
    """
    api_info = get_object_or_404(ApiInfo, id=apis_id)
    api_info.is_delete = True
    api_info.save()
    return response()


@router.get("/module/{module_id}", response=List[ApiInfoForModuleOut])
@paginate(CustomPagination)
def apis_list_for_module(request, module_id: int):
    """
    获取模块下面的接口列表
    """
    return ApiInfo.objects.filter(module_id=module_id, is_delete=False).all()


@router.post("/all/list", response=List[ApiInfoForModuleOut])
@paginate(CustomPagination)
def apis_all_list(request, data: ApiSearchIn):
    """
    获取所有接口
    """
    # 构造多条件查询条件
    query = Q() & Q(is_delete=False)
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.api_path:
        query &= Q(api_path=data.api_path)
    if data.method:
        query &= Q(method=data.method)
    return ApiInfo.objects.filter(query).all()


@router.get("/extract/list", response=List[ExtractOut])
@paginate(CustomPagination)
def extract_list(request, data: ExtractSearchIn):
    """
    查看提取器列表
    """
    query = Q()
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.project_id:
        query &= Q(httprunner_project_id=data.project_id)
    return ApiExtract.objects.filter(query).all()


@router.get("/task/demo", auth=None)
def task_demo(request):
    """
    简单celery调用示例
    """
    res = add.delay(10, 20)
    print(res.task_id)
    return response(item=res.task_id)
