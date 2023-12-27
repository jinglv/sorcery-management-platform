import json
import os
import time
from pathlib import Path

import yaml
from django.shortcuts import get_object_or_404

from apis.models import ApiExtract, ApiAssert, ApiInfo
from backend.common import response


def base_api_to_httprunner(api_name: str, api_id: int):
    """
    基础Api信息转HttpRunner json格式
    """
    api_info = get_object_or_404(ApiInfo, pk=api_id, is_delete=False)
    # 处理接口请求参数
    variables = {}
    request_info = {}
    if api_info.params_type == 'json':
        variables = json.loads(api_info.params_body.replace('\'', '"'))
        json_body = {}
        for key in variables:
            json_body.update({key: '$' + key})
        request_info = {
            'method': api_info.method.upper(),
            'url': api_info.api_path,
            'headers': {item["name"]: item["value"] for item in json.loads(api_info.header.replace('\'', '"'))},
            'json': json_body
        }
    # 查询断言信息
    test_assert = ApiAssert.objects.filter(api_id=api_info.id)
    assert_list = []
    for assert_info in test_assert:
        assert_content = assert_info.assert_extract
        if '[' in assert_content:
            assert_result = 'content.' + str_to_format(assert_content)
        else:
            assert_result = 'content.' + assert_content
        assert_data = {
            "assert_extract": assert_result,
            "expect_text": assert_info.expect_text
        }
        assert_type = assert_info.assert_type
        if assert_type == 'equal':
            assert_list.append({
                "eq": list(assert_data.values())
            })
    # 固定响应状态码为status_code=200
    assert_list.append({
        "eq": ['status_code', 200]
    })
    # 查询提取数据信息
    test_extract = ApiExtract.objects.filter(apis_id=api_info.id).all()
    extracts = []
    for extract in test_extract:
        extract_content = extract.extract
        if '[' in extract_content:
            extract_result = 'content.' + str_to_format(extract_content)
        else:
            extract_result = 'content.' + extract_content
        extracts.append({
            "name": extract.name,
            "value": extract_result
        })
    result = {
        'name': api_name,
        'base_url': "ENV_URL",
        'variables': variables,
        'request': request_info,
        'extract': {item["name"]: item["value"] for item in extracts},
        'validate': assert_list
    }
    return result


def str_to_format(format_str):
    """
    将提取只和断言值的jmespath转换为HttpRunner需求的格式
    例如：
    resp[0].accessToken -> resp.0.accessToken
    """
    # 1.根据字符串包含的[]进行分割，先'['进行分割
    step_one = format_str.split('[')
    # 2.遍历获取的数组，进行遍历，']'第二次分割
    two_result = []
    for i in step_one:
        if ']' in i:
            s = i.split(']')
            two_result.append(s)
    # 3.将字符串进行拼接
    three_result = []
    for j in two_result:
        s = '.' + j[0] + j[1]
        three_result.append(s)
    return step_one[0] + ''.join(three_result)


def dump_yaml_file(yaml_file, data):
    """
    load yaml file and check file content format
    """
    if os.path.exists(yaml_file):
        print('yml is exists')
    else:
        with open(yaml_file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream, indent=4,
                      default_flow_style=False,
                      encoding='utf-8',
                      allow_unicode=True)


def api_to_yml(project_dir, type, base_url, api_json):
    """
    生成 api yml文件
    """
    api_obj = json.loads(api_json)
    new_dict = dict()
    new_dict['name'] = api_obj.get('name')
    new_dict['base_url'] = "${ENV(" + base_url.split('=')[0] + ")}"
    if api_obj.get('variables'):
        new_dict['variables'] = api_obj.get('variables')
    new_dict['request'] = api_obj.get('request')
    if api_obj.get('extract'):
        new_dict['extract'] = api_obj.get('extract')
    if api_obj.get('validate'):
        new_dict['validate'] = api_obj.get('validate')
    if api_obj.get('setup_hooks'):
        new_dict['setup_hooks'] = api_obj.get('setup_hooks')
    if api_obj.get('teardown_hooks'):
        new_dict['teardown_hooks'] = api_obj.get('teardown_hooks')
    dump_yaml_file(project_dir + '/' + type + '/{}.yml'.format(api_obj['name'].replace(" ", "_")), new_dict)


def cases_to_yml(project_dir, type, base_url, name, config_content, cases_json):
    """
    生成 test case yml文件
    """
    new_dict = dict()
    new_dict['config'] = {}
    new_dict['teststeps'] = []
    # test case config
    new_dict['config']['name'] = name
    config_content = json.loads(config_content)
    if config_content:
        new_dict['config']['variables'] = config_content.get('validates')
    config_setup_hooks = config_content.get('setup_hooks')
    if config_setup_hooks:
        new_dict['config']['setup_hooks'] = config_setup_hooks
    config_teardown_hooks = config_content.get('teardown_hooks')
    if config_teardown_hooks:
        new_dict['config']['teardown_hooks'] = config_teardown_hooks
    if base_url:
        new_dict['config']['base_url'] = base_url.split('=')[1]
    # test case steps
    cases_json = json.loads(cases_json)
    for cases in cases_json:
        new_step = dict()
        new_step['name'] = cases.get('name')
        new_step['api'] = 'api/{}.yml'.format(cases.get('api_name').replace(" ", "_"))
        api_variables = cases.get('variables')
        if api_variables:
            new_step['variables'] = api_variables
        api_extract = cases.get('extracts')
        if api_extract:
            new_step['extract'] = api_extract
        api_validate = cases.get('validates')
        if api_validate:
            new_step['validates'] = api_validate
        new_dict['teststeps'].append(new_step)
    if len(new_dict['teststeps']) < 1:
        return response(error={"TestCase数据异常，缺少Api信息"})
    else:
        dump_yaml_file(project_dir + '/' + type + '/{}.yml'.format(name.replace(" ", "_")), new_dict)


def suite_to_yml(project_dir, type, base_url, name, config_content, suite_json):
    """
    生成 test suite yml文件
    """
    new_dict = dict()
    new_dict['config'] = {}
    new_dict['testcases'] = []
    # test case config
    new_dict['config']['name'] = name
    config_content = json.loads(config_content)
    print('config_content:', config_content)
    if config_content:
        new_dict['config']['variables'] = config_content
    if base_url:
        new_dict['config']['base_url'] = base_url.split('=')[1]
    # test case steps
    suite_json = json.loads(suite_json)
    for suite in suite_json:
        new_case = dict()
        new_case['name'] = suite.get('name')
        new_case['testcase'] = 'testcases/{}.yml'.format(suite.get('case_name').replace(" ", "_"))
        suite_params = suite.get('params')
        if suite_params:
            new_case['parameters'] = suite_params
        suite_variables = suite.get('variables')
        if suite_variables:
            new_case['variables'] = suite_variables
        new_dict['testcases'].append(new_case)
    if len(new_dict['testcases']) < 1:
        return response(error={"TestCase数据异常，缺少TestCase信息"})
    else:
        dump_yaml_file(project_dir + '/' + type + '/{}.yml'.format(name.replace(" ", "_")), new_dict)


def summary_to_dict(summary_json, report_name):
    """
    summary 重新转字典
    :param summary_json: 从数据库读取的 json 格式 summary
    :param report_name: 报告名称
    :return:
    """
    summary = json.loads(summary_json.replace('&#34;', r'\"'))
    summary['html_report_name'] = report_name
    try:
        summary["time"]["start_at"] = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime(summary["time"]["start_at"]))
        summary["time"]["start_datetime"] = summary["time"]["start_at"]
    except:
        pass
    return summary


def del_file(path, all=True):
    """
    删除指定目录下所有文件
    """
    try:
        if all:
            for elm in Path(path).glob('*'):
                elm.unlink()
        else:
            print('path:', path)
            if os.path.exists(path):
                filePath = Path(path)
                filePath.unlink()
    except OSError as e:
        print(f"Error:{e.strerror}")
