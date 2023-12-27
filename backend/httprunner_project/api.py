import io
import json
import os
import pathlib
import platform
import subprocess
import time
import traceback
import uuid
from typing import List

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from httprunner.api import HttpRunner
from ninja import Router
from ninja.pagination import paginate

from apis.models import ApiInfo
from backend.common import response, Error, model_to_dict
from backend.pagination import CustomPagination
from backend.settings import HTTP_RUNNER_PROJECT_DIR
from httprunner_project.api_helper import httprunner_file_code_content, debugtalk_code, env_code
from httprunner_project.models import HttpRunnerProjectInfo, HttpRunnerApiInfo, HttpRunnerRunInfo, HttpRunnerProcessor, \
    HttpRunnerTestCaseInfo, HttpRunnerSuiteInfo
from httprunner_project.schema import HttpRunnerProjectInfoIn, HttpRunnerProjectInfoOut, DebugTalkCodeIn, \
    HttpRunnerApiInfoIn, HttpRunnerApiRunIn, HttpRunnerApiResultListOut, \
    HttpRunnerUpdateApiInfoIn, HttpRunnerTestCaseIn, HttpRunnerCasesRunIn, HttpRunnerSuiteIn, HttpRunnerListOut, \
    HttpRunnerSearchIn, HttpRunnerSuiteRunIn
from httprunner_project.utils import base_api_to_httprunner, api_to_yml, summary_to_dict, del_file, cases_to_yml, \
    suite_to_yml
from project.models import Project

router = Router(tags=["httprunner"])


@router.post("/project/create")
@transaction.atomic
def create_httprunner_project(request, data: HttpRunnerProjectInfoIn):
    """
    创建httpRunner项目
    """
    # 查询项目是否存在
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    # 保存HttpRunner项目信息
    httprunner_project_info = HttpRunnerProjectInfo.objects.create(**data.dict())
    # 创建HttpRunner工程
    project_dir = HTTP_RUNNER_PROJECT_DIR
    # 判断项目工程是否已创建
    if os.path.exists(project_dir + data.name):
        return response(item='HttpRunner项目已创建，请勿重复创建')
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        # 系统为Linux
        subprocess.Popen(f'cd {project_dir} \n hrun --startproject {data.name}',
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    else:
        # window系统
        subprocess.Popen(['cd', project_dir],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
        subprocess.Popen(['hrun --startproject', data.name],
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return response(item=model_to_dict(httprunner_project_info))


@router.put("/project/{httprunner_project_id}")
@transaction.atomic
def update_httprunner_project(request, httprunner_project_id: int, payload: HttpRunnerProjectInfoIn):
    """
    更新httpRunner项目
    """
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=httprunner_project_id)
    for attr, value in payload.dict().items():
        setattr(httprunner_project, attr, value)
    httprunner_project.save()
    # 查询保存之后的信息
    query_result = list(HttpRunnerProjectInfo.objects.filter(id=httprunner_project_id).values())[0]
    # 判断已创建了工程
    http_runner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    if os.path.exists(http_runner_project_dir):
        debug_talk_file = http_runner_project_dir + "/debugtalk.py"
        with open(debug_talk_file, 'w', encoding='utf-8') as file:
            file.write(query_result.get('code'))

    env_file = http_runner_project_dir + "/.env"
    with open(env_file, 'w', encoding='utf-8') as file:
        file.write(query_result.get('env_code'))
    return response()


@router.get("/projects", response=List[HttpRunnerProjectInfoOut])
@paginate(CustomPagination)
def httprunner_project_list(request, **kwargs):
    """
    项目列表
    """
    project_info_list = HttpRunnerProjectInfo.objects.all()
    project_info = []
    for i in project_info_list:
        project_id = i.project_id
        project = Project.objects.get(pk=project_id)
        project_name = project.name
        project = {
            "id": i.id,
            "project_id": project_id,
            "project_name": project_name,
            "name": i.name,
            "describe": i.describe,
            "env_code": i.env_code,
            "code": i.code,
            "create_time": i.create_time,
            "update_time": i.update_time
        }
        project_info.append(project)
    return project_info


@router.post("/code/run")
def run_python_code(request, data: DebugTalkCodeIn):
    """
    python code执行
    """
    # 1.将传入的Python代码写到一个Python文件中
    python_file = "python_" + str(uuid.uuid4()) + ".py"
    fp = open(python_file, 'w', encoding='utf-8')
    fp.write(data.code)
    fp.close()
    # 2.运行Python文件
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        # 系统为Linux
        p = subprocess.Popen(f'python {python_file}',
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p.wait()
        out = p.stdout.read()
        res = out.decode('utf-8')
        print('run res:', res)
    else:
        # window系统
        p = subprocess.Popen(['python', python_file],
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        # 输出stdout
        result = p.communicate()[0]
        try:
            res = result.decode('utf-8')
        except UnicodeDecodeError:
            res = result.decode('gb2312')
    # 删除文件
    os.remove(python_file)
    return response(item=res)


@router.post("/apis/create")
def httprunner_save_api(request, data: HttpRunnerApiInfoIn):
    """
    保存HttpRunner对应结构接口信息
    """
    httpruuner_api_info = HttpRunnerApiInfo.objects.filter(pk=data.base_api_id)
    if len(httpruuner_api_info) > 0:
        return response()
    get_object_or_404(HttpRunnerProjectInfo, pk=data.httprunner_project_id)
    api_info = base_api_to_httprunner(data.name, data.base_api_id)
    HttpRunnerApiInfo.objects.create(
        name=data.name,
        api_id=data.base_api_id,
        api_info=api_info,
        httprunner_project_id=data.httprunner_project_id
    )
    return response()


@router.get("/apis/detail/{api_id}")
def httprunner_api_detail(request, api_id: int):
    """
    HttpRunner接口详情
    """
    httprunner_api_info = get_object_or_404(HttpRunnerApiInfo, pk=api_id)
    api_info = get_object_or_404(ApiInfo, pk=httprunner_api_info.api_id)
    processor_codes = HttpRunnerProcessor.objects.filter(httprunner_id=api_id).filter(type='API').all()
    pre_processor = ''
    post_processor = ''
    for code in processor_codes:
        if code.processor_type == 'PRE':
            pre_processor = code.processor_code
        elif code.processor_type == 'POST':
            post_processor = code.processor_code
    data = {
        "id": httprunner_api_info.id,
        "name": httprunner_api_info.name,
        "base_api_id": api_info.id,
        "base_api_name": api_info.name,
        "api_info": json.loads(httprunner_api_info.api_info.replace('\'', '"')),
        "pre_processor": pre_processor,
        "post_processor": post_processor,
        "create_time": httprunner_api_info.create_time
    }
    return response(item=data)


@router.put("/apis/update/{api_id}")
def httprunner_update_api(request, api_id: int, data: HttpRunnerUpdateApiInfoIn):
    """
    更新HttpRunner接口信息
    """
    httprunner_api_info = get_object_or_404(HttpRunnerApiInfo, pk=api_id)
    HttpRunnerApiInfo.objects.filter(pk=api_id).update(
        name=data.name,
        api_info=data.api_info
    )
    if (data.pre_processor is not None and data.pre_processor != "") or (
            data.post_processor is not None and data.post_processor != ""):
        # 截取代码中的方法名
        setup_method_name = (data.pre_processor.split()[1])[:-3]
        teardown_method_name = (data.post_processor.split()[1])[:-3]
        debugtalk_code(httprunner_api_info.httprunner_project_id, data.pre_processor, data.post_processor, api_id,
                       'API')
        info = json.loads(json.dumps(data.api_info))
        info['setup_hooks'] = ['${' + setup_method_name + '()}']
        info['teardown_hooks'] = ['${' + teardown_method_name + '()}']
        HttpRunnerApiInfo.objects.filter(pk=api_id).update(
            name=data.name,
            api_info=info
        )
    return response()


@router.delete("/apis/delete/{api_id}")
@transaction.atomic
def httprunner_delete_api(request, api_id: int):
    """
    更新HttpRunner接口信息
    """
    httprunner_api_info = get_object_or_404(HttpRunnerApiInfo, pk=api_id)
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_api_info.httprunner_project_id)
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    api_dir = httprunner_project_dir + '/api/'
    api_yml_file = api_dir + httprunner_api_info.name.replace(" ", "_") + '.yml'
    del_file(api_yml_file, all=False)
    httprunner_api_info.delete()
    return response()


@router.post("/apis/list", response=List[HttpRunnerListOut])
@paginate(CustomPagination)
def httprunner_api_list(request, data: HttpRunnerSearchIn):
    """
    HttpRunner接口详情
    """
    # 构造查询条件
    query = Q()
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.httprunner_project_id:
        query &= Q(httprunner_project_id=data.httprunner_project_id)
    httprunner_apis = HttpRunnerApiInfo.objects.filter(query).all()
    httprunner_api_list = []
    for httprunner_api in httprunner_apis:
        httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_api.httprunner_project_id)
        http_runner_info = HttpRunnerRunInfo.objects.filter(ids__contains=httprunner_api.id).filter(
            type='API').last()
        data = {
            "id": httprunner_api.id,
            "name": httprunner_api.name,
            "httprunner_project_name": httprunner_project.name,
            "status": http_runner_info.result if http_runner_info is not None else 'non',
            "report_name": http_runner_info.name if http_runner_info is not None else '',
            "create_time": httprunner_api.create_time
        }
        httprunner_api_list.append(data)
    return httprunner_api_list


@router.get("/apis/ids/{project_id}")
def httprunner_api_ids(request, project_id: int):
    """
    查询项目下接口集合
    """
    httprunner_apis = HttpRunnerApiInfo.objects.filter(httprunner_project_id=project_id)
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=project_id)
    httprunner_api_list = []
    for httprunner_api in httprunner_apis:
        data = {
            "id": httprunner_api.id,
            "name": httprunner_api.name,
            "httprunner_project_name": httprunner_project.name,
            "create_time": httprunner_api.create_time
        }
        httprunner_api_list.append(data)
    return response(item=httprunner_api_list)


@router.post("/apis/run")
def httprunner_run_api(request, data: HttpRunnerApiRunIn):
    """
    执行接口
    """
    # 1 根据项目id，查询项目配置数据，进行配置数据处理
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=data.httprunner_project_id)
    # 1.1 拼接HttpRunner工程目录地址
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    # 1.2 传入的环境地址（格式为：test=http://xxxx.xxx.xxx）截取环境地址名称，与HttpRunner工程中.env文件中的内容进行处理
    env_code(data.httprunner_project_id, data.env_url, data.env_url)
    # 1.4 拼接 HttpRunner工程目录下的api和.env
    api_dir = httprunner_project_dir + '/api/'
    env_dir = httprunner_project_dir + '/.env'
    # 2 遍历传入的HttpRunner接口的id集合，并生成HttpRunner工程目录下api下对应接口的yml文件
    # 2.1 将api目录下所有文件删除
    del_file(api_dir)
    for api_id in data.api_ids:
        # 2.2 根据接口id，查询接口信息
        httprunner_api_info = get_object_or_404(HttpRunnerApiInfo, pk=api_id)
        # 2.3 将接口信息json转为yaml并保存文件
        api_to_yml(httprunner_project_dir, 'api', data.env_url, httprunner_api_info.api_info.replace('\'', '"'))
        # 2.4 验证环境信息已经成功写入.env文件中
        with open(env_dir, "r") as file:
            env_content = file.read()
        api_yml_file = httprunner_api_info.name.replace(" ", "_") + '.yml'
        # 2.5 验证生成的yaml文件是否存在
        if os.path.exists(api_dir + api_yml_file) and data.env_url in env_content:
            print(api_dir + api_yml_file + ',成功生成文件！')
    # 3 接口执行
    logs_dir = httprunner_project_dir + '/logs'
    logs_dir_obj = pathlib.Path(logs_dir)
    if not os.path.exists(logs_dir):
        logs_dir_obj.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir_obj.joinpath('logs', 'test.log')
    runner = HttpRunner(
        # failfast=False,
        # save_tests=True,
        log_level="DEBUG",
        # 地址必须是str
        log_file=str(log_path.resolve()))
    try:
        summary = runner.run(path_or_tests=api_dir, dot_env_path=env_dir)
    except Exception as e:
        f = io.StringIO()
        traceback.print_exc(file=f)
        summary = {
            "success": 'error',
            "log": f.getvalue(),
        }
        f.close()
    api_run_result = summary.get("success", None)
    if api_run_result == "error":
        result = "error"
    elif api_run_result:
        result = "success"
    else:
        result = "fail"
    # 结果入库
    HttpRunnerRunInfo.objects.create(
        name=time.strftime("%Y%m%d%H%M%S", time.localtime()),
        ids=data.api_ids,
        type=data.type,
        summary=json.dumps(summary, ensure_ascii=False),
        result=result
    )
    return response(item=summary)


@router.put("/apis/{api_id}")
def httprunner_update_base_api(request, api_id: int, data: HttpRunnerApiInfoIn):
    """
    保存HttpRunner对应结构接口信息
    """
    get_object_or_404(HttpRunnerApiInfo, pk=api_id)
    api_info = base_api_to_httprunner(data.name, data.base_api_id)
    HttpRunnerApiInfo.objects.filter(pk=api_id).update(
        name=data.name,
        api_id=data.base_api_id,
        api_info=api_info,
        httprunner_project_id=data.httprunner_project_id
    )
    return response()


@router.get("/report/render/{run_name}")
def render_case_report(request, run_name: str):
    """
    渲染生成报告
    """
    httprunner_run_info = get_object_or_404(HttpRunnerRunInfo, name=run_name)
    summary = summary_to_dict(httprunner_run_info.summary, httprunner_run_info.name)
    return render(request, 'extent_report.html', context=summary)


@router.get("/apis/result/list/{type}", response=List[HttpRunnerApiResultListOut])
@paginate(CustomPagination)
def httprunner_run_result_list(request, type: str):
    """
    HttpRunner接口执行结果
    """
    # 查询所有执行结果数据
    run_infos = HttpRunnerRunInfo.objects.filter(type=type).order_by('-create_time').all()
    result = []
    for run_info in run_infos:
        id_list = json.loads(run_info.ids)
        ids = []
        if type == 'API':
            for id in id_list:
                api_info = get_object_or_404(HttpRunnerApiInfo, pk=id)
                ids.append({
                    'id': id,
                    'name': api_info.name
                })
        elif type == 'TESTCASE':
            for id in id_list:
                case_info = get_object_or_404(HttpRunnerTestCaseInfo, pk=id)
                ids.append({
                    'id': id,
                    'name': case_info.name
                })
        result.append({
            'id': run_info.id,
            'name': run_info.name,
            'type': run_info.type,
            'result': run_info.result,
            'ids': ids,
            'create_time': run_info.create_time
        })
    return result


@router.post("/cases/create")
@transaction.atomic
def httprunner_save_test_case(request, data: HttpRunnerTestCaseIn):
    """
    保存HttpRunner对应结构测试用例信息
    """
    test_case_list = []
    for test_case_info in data.test_case_infos:
        api_info = get_object_or_404(HttpRunnerApiInfo, id=test_case_info.api_id)
        test_case = dict()
        test_case['name'] = test_case_info.name
        test_case['api_id'] = test_case_info.api_id
        test_case['api_name'] = api_info.name
        if test_case_info.variables:
            test_case['variables'] = test_case_info.variables
        if test_case_info.extracts:
            test_case['extracts'] = test_case_info.extracts
        if test_case_info.validates:
            test_case['validates'] = test_case_info.validates
        test_case_list.append(test_case)
    # 保存测试用例基础信息
    if data.public_variables:
        public_variables_dict = {'variables': data.public_variables}
    else:
        public_variables_dict = {}
    HttpRunnerTestCaseInfo.objects.create(
        httprunner_project_id=data.httprunner_project_id,
        name=data.name,
        config_content=public_variables_dict,
        test_case_info=test_case_list
    )
    # 查询已保存的测试用例基础信息
    test_case = get_object_or_404(HttpRunnerTestCaseInfo, name=data.name)
    test_case_id = test_case.id
    if (data.pre_processor is not None and data.pre_processor != "") or (
            data.post_processor is not None and data.post_processor != ""):
        # 截取代码中的方法名
        setup_method_name = (data.pre_processor.split()[1])[:-3]
        teardown_method_name = (data.post_processor.split()[1])[:-3]
        debugtalk_code(data.httprunner_project_id, data.pre_processor, data.post_processor, test_case_id,
                       'TESTCASE')
        public_variables_dict['setup_hooks'] = ['${' + setup_method_name + '()}']
        public_variables_dict['teardown_hooks'] = ['${' + teardown_method_name + '()}']
        HttpRunnerTestCaseInfo.objects.filter(pk=test_case_id).update(config_content=public_variables_dict)
    return response()


@router.put("/cases/update/{test_case_id}")
@transaction.atomic
def httprunner_update_test_case(request, test_case_id: int, data: HttpRunnerTestCaseIn):
    """
    保存HttpRunner对应结构测试用例信息
    """
    get_object_or_404(HttpRunnerTestCaseInfo, pk=test_case_id)
    test_case_list = []
    for test_case_info in data.test_case_infos:
        api_info = get_object_or_404(HttpRunnerApiInfo, id=test_case_info.api_id)
        test_case = dict()
        test_case['api_id'] = test_case_info.api_id
        test_case['api_name'] = api_info.name
        if test_case_info.variables:
            test_case['variables'] = test_case_info.variables
        if test_case_info.extracts:
            test_case['extracts'] = test_case_info.extracts
        if test_case_info.validates:
            test_case['validates'] = test_case_info.validates
        test_case_list.append(test_case)
    # 保存测试用例基础信息
    if data.public_variables:
        public_variables_dict = {'validates': data.public_variables}
    else:
        public_variables_dict = {}
    HttpRunnerTestCaseInfo.objects.filter(pk=test_case_id).update(
        name=data.name,
        httprunner_project_id=data.httprunner_project_id,
        config_content=public_variables_dict,
        test_case_info=test_case_list
    )
    if (data.pre_processor is not None and data.pre_processor != "") or (
            data.post_processor is not None and data.post_processor != ""):
        # 截取代码中的方法名
        setup_method_name = (data.pre_processor.split()[1])[:-3]
        teardown_method_name = (data.post_processor.split()[1])[:-3]
        debugtalk_code(data.httprunner_project_id, data.pre_processor, data.post_processor, test_case_id,
                       'TESTCASE')
        public_variables_dict['setup_hooks'] = ['${' + setup_method_name + '()}']
        public_variables_dict['teardown_hooks'] = ['${' + teardown_method_name + '()}']
        HttpRunnerTestCaseInfo.objects.filter(pk=test_case_id).update(config_content=public_variables_dict)
    return response()


@router.delete("/cases/delete/{test_case_id}")
@transaction.atomic
def httprunner_delete_test_case(request, test_case_id: int):
    """
    更新HttpRunner接口信息
    1.删除测试用例基础信息
    2.删除测试用例testcases目录下yml文件
    3.删除testcases关联的处理器代码和debugtalk里面的代码
    4.删除测试结果中包含test_case_id的数据
    """
    # 1. 获取testcase基础信息
    httprunner_test_case_info = get_object_or_404(HttpRunnerTestCaseInfo, pk=test_case_id)
    # 1.1 删除数据库testcase用例信息
    httprunner_test_case_info.delete()
    # 2. 获取HttpRunner项目信息
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_test_case_info.httprunner_project_id)
    # 2.1 组装对应的testcase下 yml文件
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    test_case_dir = httprunner_project_dir + '/testcases/'
    case_yml_file = test_case_dir + httprunner_test_case_info.name.replace(" ", "_") + '.yml'
    # 2.2 删除指定的文件
    del_file(case_yml_file, all=False)
    # 3. 获取前置和后置代码
    cases_processor_codes = HttpRunnerProcessor.objects.filter(httprunner_id=test_case_id).filter(type='TESTCASE').all()
    # 3.1 删除debugtalk.py中的代码
    for case_code in cases_processor_codes:
        if case_code.processor_type == 'PRE':
            pre_codes = case_code.processor_code
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', case_code.name, "", pre_codes)
        elif case_code.processor_type == 'POST':
            post_codes = case_code.processor_code
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', case_code.name, "", post_codes)
    # 3.2 删除数据库数据
    cases_processor_codes.delete()
    # 4.删除测试结果
    test_case_run_info = HttpRunnerRunInfo.objects.filter(ids__contains=test_case_id).filter(type='TESTCASE').all()
    test_case_run_info.delete()
    return response()


@router.post("/cases/list", response=List[HttpRunnerListOut])
@paginate(CustomPagination)
def httprunner_cases_list(request, data: HttpRunnerSearchIn):
    """
    HttpRunner接口详情
    """
    # 构造查询条件
    query = Q()
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.httprunner_project_id:
        query &= Q(httprunner_project_id=data.httprunner_project_id)
    httprunner_cases = HttpRunnerTestCaseInfo.objects.filter(query).all()
    httprunner_api_list = []
    for httprunner_case in httprunner_cases:
        httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_case.httprunner_project_id)
        http_runner_info = HttpRunnerRunInfo.objects.filter(ids__contains=httprunner_case.id).filter(
            type='TESTCASE').last()
        data = {
            "id": httprunner_case.id,
            "name": httprunner_case.name,
            "httprunner_project_name": httprunner_project.name,
            "status": http_runner_info.result if http_runner_info is not None else 'non',
            "report_name": http_runner_info.name if http_runner_info is not None else '',
            "create_time": httprunner_case.create_time
        }
        httprunner_api_list.append(data)
    return httprunner_api_list


@router.get("/cases/detail/{case_id}")
def httprunner_cases_detail(request, case_id: int):
    """
    HttpRunner接口详情
    """
    httprunner_cases_info = get_object_or_404(HttpRunnerTestCaseInfo, pk=case_id)
    cases_processor_codes = HttpRunnerProcessor.objects.filter(httprunner_id=case_id).filter(type='TESTCASE').all()
    pre_processor = ''
    post_processor = ''
    for code in cases_processor_codes:
        if code.processor_type == 'PRE':
            pre_processor = code.processor_code
        elif code.processor_type == 'POST':
            post_processor = code.processor_code
    variables = json.loads(httprunner_cases_info.config_content.replace('\'', '"'))
    data = {
        "httprunner_project_id": httprunner_cases_info.httprunner_project_id,
        "id": httprunner_cases_info.id,
        "name": httprunner_cases_info.name,
        "config": {} if variables.get('variables') is None else variables.get('variables'),
        "teststeps": httprunner_cases_info.test_case_info,
        "pre_processor": pre_processor,
        "post_processor": post_processor,
        "create_time": httprunner_cases_info.create_time
    }
    return response(item=data)


@router.post("/cases/run")
def httprunner_run_cases(request, data: HttpRunnerCasesRunIn):
    """
    执行测试用例
    """
    # 1 根据项目id，查询项目配置数据，进行配置数据处理
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=data.httprunner_project_id)
    # 1.1 拼接HttpRunner工程目录地址
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    # 1.2 传入的环境地址（格式为：test=http://xxxx.xxx.xxx）截取环境地址名称，与HttpRunner工程中.env文件中的内容进行处理
    env_code(data.httprunner_project_id, data.env_url, data.env_url)
    # 1.4 拼接 HttpRunner工程目录下的testcasse api和.env，注：在生成testcase yml同时，也需要将api yml删除在生成，避免testcase和api不一致的情况
    cases_dir = httprunner_project_dir + '/testcases/'
    api_dir = httprunner_project_dir + '/api/'
    env_dir = httprunner_project_dir + '/.env'
    del_file(cases_dir)
    del_file(api_dir)
    # 2 遍历传入的HttpRunner用例的id集合，并生成HttpRunner工程目录下testcase下对应接口的yml文件
    for case_id in data.cases_ids:
        # 2.1 根据用例id，查询用例信息
        httprunner_cases_info = get_object_or_404(HttpRunnerTestCaseInfo, pk=case_id)
        api_infos = json.loads(httprunner_cases_info.test_case_info.replace('\'', '"'))
        for api_info in api_infos:
            api_id = api_info.get('api_id')
            # 2.2 根据接口id，查询接口信息
            httprunner_api_info = get_object_or_404(HttpRunnerApiInfo, pk=api_id)
            # 2.3 将接口信息json转为yaml并保存文件
            api_to_yml(httprunner_project_dir, 'api', data.env_url, httprunner_api_info.api_info.replace('\'', '"'))
            # 2.4 验证环境信息已经成功写入.env文件中
            with open(env_dir, "r") as file:
                env_content = file.read()
            # 2.5 验证生成的yaml文件是否存在
            if os.path.exists(api_dir + httprunner_api_info.name + '.yml') and data.env_url in env_content:
                print(api_dir + httprunner_api_info.name + '.yml' + ',成功生成文件！')
        case_name = httprunner_cases_info.name
        # 2.2 将接口信息json转为yaml并保存文件
        cases_to_yml(httprunner_project_dir, 'testcases', data.env_url, case_name,
                     httprunner_cases_info.config_content.replace('\'', '"'),
                     httprunner_cases_info.test_case_info.replace('\'', '"'))
        # 2.3 验证环境信息已经成功写入.env文件中
        with open(env_dir, "r") as file:
            env_content = file.read()
        case_yml_file = case_name.replace(" ", "_") + '.yml'
        # 2.4 验证生成的yaml文件是否存在
        if os.path.exists(cases_dir + case_yml_file) and data.env_url in env_content:
            print(cases_dir + case_yml_file + ',成功生成文件！')
    # 3 接口执行
    logs_dir = httprunner_project_dir + '/logs'
    logs_dir_obj = pathlib.Path(logs_dir)
    if not os.path.exists(logs_dir):
        logs_dir_obj.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir_obj.joinpath('logs', 'test.log')
    runner = HttpRunner(
        # failfast=False,
        # save_tests=True,
        log_level="DEBUG",
        # 地址必须是str
        log_file=str(log_path.resolve()))
    try:
        summary = runner.run(path_or_tests=cases_dir, dot_env_path=env_dir)
    except Exception as e:
        f = io.StringIO()
        traceback.print_exc(file=f)
        summary = {
            "success": 'error',
            "log": f.getvalue(),
        }
        f.close()
    api_run_result = summary.get("success", None)
    if api_run_result == "error":
        result = "error"
    elif api_run_result:
        result = "success"
    else:
        result = "fail"
    # 结果入库
    HttpRunnerRunInfo.objects.create(
        name=time.strftime("%Y%m%d%H%M%S", time.localtime()),
        ids=data.cases_ids,
        type=data.type,
        summary=json.dumps(summary, ensure_ascii=False),
        result=result
    )
    return response(item=summary)


@router.get("/cases/ids/{project_id}")
def httprunner_test_case_ids(request, project_id: int):
    """
    查询项目下测试用例集合
    """
    httprunner_test_cases = HttpRunnerTestCaseInfo.objects.filter(httprunner_project_id=project_id)
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=project_id)
    httprunner_test_case_list = []
    for httprunner_test_case in httprunner_test_cases:
        data = {
            "id": httprunner_test_case.id,
            "name": httprunner_test_case.name,
            "httprunner_project_name": httprunner_project.name,
            "create_time": httprunner_test_case.create_time
        }
        httprunner_test_case_list.append(data)
    return response(item=httprunner_test_case_list)


@router.post("/suite/create")
@transaction.atomic
def httprunner_save_suite(request, data: HttpRunnerSuiteIn):
    """
    保存HttpRunner对应结构测试用例信息
    """
    test_suite_list = []
    for case in data.test_cases:
        case_info = get_object_or_404(HttpRunnerTestCaseInfo, id=case.case_id)
        test_case = dict()
        test_case['name'] = case.name
        test_case['case_id'] = case.case_id
        test_case['case_name'] = case_info.name
        if case.variables:
            test_case['variables'] = case.variables
        if case.params:
            test_case['params'] = case.params
        test_suite_list.append(test_case)
    HttpRunnerSuiteInfo.objects.create(
        httprunner_project_id=data.httprunner_project_id,
        name=data.name,
        config_content=data.public_variables,
        suite_info=test_suite_list
    )
    return response()


@router.put("/suite/update/{suite_id}")
@transaction.atomic
def httprunner_update_suite(request, suite_id: int, data: HttpRunnerSuiteIn):
    """
    保存HttpRunner对应结构测试用例信息
    """
    get_object_or_404(HttpRunnerSuiteInfo, pk=suite_id)
    test_case_list = []
    for test_case_info in data.test_cases:
        case_info = get_object_or_404(HttpRunnerTestCaseInfo, id=test_case_info.case_id)
        test_case = dict()
        test_case['case_id'] = test_case_info.case_id
        test_case['name'] = test_case_info.name
        if test_case_info.variables:
            test_case['variables'] = test_case_info.variables
        if test_case_info.params:
            test_case['params'] = test_case_info.params
        test_case_list.append(test_case)
    HttpRunnerSuiteInfo.objects.filter(pk=suite_id).update(
        name=data.name,
        httprunner_project_id=data.httprunner_project_id,
        config_content=data.public_variables,
        suite_info=test_case_list
    )
    return response()


@router.post("/suite/list", response=List[HttpRunnerListOut])
@paginate(CustomPagination)
def httprunner_suite_list(request, data: HttpRunnerSearchIn):
    """
    HttpRunner接口详情
    """
    # 构造查询条件
    query = Q()
    if data.name:
        query &= Q(name__icontains=data.name)
    if data.httprunner_project_id:
        query &= Q(httprunner_project_id=data.httprunner_project_id)
    httprunner_suites = HttpRunnerSuiteInfo.objects.filter(query).all()
    httprunner_suite_list = []
    for httprunner_suite in httprunner_suites:
        httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_suite.httprunner_project_id)
        http_runner_info = HttpRunnerRunInfo.objects.filter(ids__contains=httprunner_suite.id).filter(
            type='TESTSUITE').last()
        data = {
            "id": httprunner_suite.id,
            "name": httprunner_suite.name,
            "httprunner_project_name": httprunner_project.name,
            "status": http_runner_info.result if http_runner_info is not None else 'non',
            "report_name": http_runner_info.name if http_runner_info is not None else '',
            "create_time": httprunner_suite.create_time
        }
        httprunner_suite_list.append(data)
    return httprunner_suite_list


@router.get("/suite/detail/{suite_id}")
def httprunner_suite_detail(request, suite_id: int):
    """
    HttpRunner接口详情
    """
    httprunner_suite_info = get_object_or_404(HttpRunnerSuiteInfo, pk=suite_id)
    data = {
        "httprunner_project_id": httprunner_suite_info.httprunner_project_id,
        "id": httprunner_suite_info.id,
        "name": httprunner_suite_info.name,
        "config": httprunner_suite_info.config_content,
        "test_cases": httprunner_suite_info.suite_info,
        "create_time": httprunner_suite_info.create_time
    }
    return response(item=data)


@router.delete("/suite/delete/{suite_id}")
@transaction.atomic
def httprunner_delete_suite(request, suite_id: int):
    """
    更新HttpRunner接口信息
    1.删除测试用例基础信息
    2.删除测试用例testsuites目录下yml文件
    3.删除测试结果中包含suite_id的数据
    """
    # 1. 获取testcase基础信息
    httprunner_suite_info = get_object_or_404(HttpRunnerSuiteInfo, pk=suite_id)
    # 1.1 删除数据库testcase用例信息
    httprunner_suite_info.delete()
    # 2. 获取HttpRunner项目信息
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, pk=httprunner_suite_info.httprunner_project_id)
    # 2.1 组装对应的testcase下 yml文件
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    suite_dir = httprunner_project_dir + '/testsuites/'
    suite_yml_file = suite_dir + httprunner_suite_info.name.replace(" ", "_") + '.yml'
    # 2.2 删除指定的文件
    del_file(suite_yml_file, all=False)
    # 4.删除测试结果
    suite_run_info = HttpRunnerRunInfo.objects.filter(ids__contains=suite_id).filter(type='TESTSUITE').all()
    suite_run_info.delete()
    return response()


@router.post("/suite/run")
@transaction.atomic
def httprunner_run_suite(request, data: HttpRunnerSuiteRunIn):
    """
    执行测试用例
    """
    # 1 根据项目id，查询项目配置数据，进行配置数据处理
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=data.httprunner_project_id)
    # 1.1 拼接HttpRunner工程目录地址
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name
    # 1.2 传入的环境地址（格式为：test=http://xxxx.xxx.xxx）截取环境地址名称，与HttpRunner工程中.env文件中的内容进行处理
    env_code(data.httprunner_project_id, data.env_url, data.env_url)
    # 1.4 拼接 HttpRunner工程目录下的testsuites api和.env，注：在生成testcase yml同时，也需要将api yml删除在生成，避免testcase和api不一致的情况
    suite_dir = httprunner_project_dir + '/testsuites/'
    env_dir = httprunner_project_dir + '/.env'
    del_file(suite_dir)
    # 2 遍历传入的HttpRunner用例的id集合，并生成HttpRunner工程目录下testcase下对应接口的yml文件
    for suite_id in data.suite_ids:
        # 2.1 根据用例id，查询用例信息
        httprunner_suite_info = get_object_or_404(HttpRunnerSuiteInfo, pk=suite_id)
        suite_name = httprunner_suite_info.name
        # 2.2 将接口信息json转为yaml并保存文件
        suite_to_yml(httprunner_project_dir, 'testsuites', data.env_url, suite_name,
                     httprunner_suite_info.config_content.replace('\'', '"'),
                     httprunner_suite_info.suite_info.replace('\'', '"'))
        # 2.3 验证环境信息已经成功写入.env文件中
        with open(env_dir, "r") as file:
            env_content = file.read()
        suite_yml_file = suite_name.replace(" ", "_") + '.yml'
        # 2.4 验证生成的yaml文件是否存在
        if os.path.exists(suite_dir + suite_yml_file) and data.env_url in env_content:
            print(suite_dir + suite_yml_file + ',成功生成文件！')
    # 3 接口执行
    logs_dir = httprunner_project_dir + '/logs'
    logs_dir_obj = pathlib.Path(logs_dir)
    if not os.path.exists(logs_dir):
        logs_dir_obj.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir_obj.joinpath('logs', 'test.log')
    runner = HttpRunner(
        # failfast=False,
        # save_tests=True,
        log_level="DEBUG",
        # 地址必须是str
        log_file=str(log_path.resolve()))
    try:
        summary = runner.run(path_or_tests=suite_dir, dot_env_path=env_dir)
    except Exception as e:
        f = io.StringIO()
        traceback.print_exc(file=f)
        summary = {
            "success": 'error',
            "log": f.getvalue(),
        }
        f.close()
    api_run_result = summary.get("success", None)
    if api_run_result == "error":
        result = "error"
    elif api_run_result:
        result = "success"
    else:
        result = "fail"
    # 结果入库
    HttpRunnerRunInfo.objects.create(
        name=time.strftime("%Y%m%d%H%M%S", time.localtime()),
        ids=data.suite_ids,
        type=data.type,
        summary=json.dumps(summary, ensure_ascii=False),
        result=result
    )
    return response(item=summary)
