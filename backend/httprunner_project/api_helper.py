from django.shortcuts import get_object_or_404

from backend.settings import HTTP_RUNNER_PROJECT_DIR
from httprunner_project.models import HttpRunnerProcessor, HttpRunnerProjectInfo


def httprunner_file_code_content(dir_name, file_name, method_name, new_code, old_codes=None):
    """
    HttpRunner工程中文件数据处理
    :file_name debugtalk env
    """
    # 读取HttpRunner工程中的文件
    httprunner_project_dir = HTTP_RUNNER_PROJECT_DIR + dir_name
    code_file = httprunner_project_dir + file_name
    # 读取文件中所有内容
    with open(code_file, "r") as file:
        all_content = file.read()
    # 判断方法是否存在，不存在则进行追加，存在则将原有内容删除在追加
    if len(all_content) == 0:
        with open(code_file, 'a', encoding='utf-8') as file:
            file.write(new_code)
    elif len(all_content) != 0 and method_name not in all_content:
        with open(code_file, 'a', encoding='utf-8') as file:
            file.write("\n")
            file.write(new_code)
    else:
        if old_codes is not None:
            # 删除原有内容，注意删除后的空行问题
            content = all_content.replace(old_codes, "").rstrip('\n')
            if len(content) == 0:
                with open(code_file, 'w', encoding='utf-8') as file:
                    file.write(new_code)
            else:
                with open(code_file, 'w', encoding='utf-8') as file:
                    file.write(content + "\n" + new_code)


def debugtalk_code(project_id, pre_processor_code, post_processor_code, id, type):
    """
    辅助函数处理
    @param: project_id HttpRunner Project Id
    @param: pre_processor_code 前置处理器代码
    @param: post_processor_code 后置处理器代码
    @param: id 处理器代码的保存数据表的httprunner_id
    @parma：type 处理器代码类型 API-接口 TESTCASE-测试用例 TESTSUITE-测试用例集
    """
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=project_id)
    if pre_processor_code is not None or post_processor_code is not None:
        # 截取代码中的方法名
        setup_method_name = (pre_processor_code.split()[1])[:-3]
        teardown_method_name = (post_processor_code.split()[1])[:-3]
        # 查询代码是否已保存在数据库
        search_pre_code = HttpRunnerProcessor.objects.filter(name=setup_method_name).filter(httprunner_id=id).filter(
            type=type)
        if len(search_pre_code) > 0:
            # 前置代码已存在，数据进行更新
            HttpRunnerProcessor.objects.filter(name=setup_method_name).filter(httprunner_id=id).filter(
                type=type).update(processor_code=pre_processor_code)
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', setup_method_name,
                                         search_pre_code[0].processor_code, pre_processor_code)
        else:
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', setup_method_name,
                                         post_processor_code)
            HttpRunnerProcessor.objects.create(
                name=setup_method_name,
                type=type,
                processor_type='PRE',
                processor_code=pre_processor_code,
                httprunner_id=id
            )
        search_post_code = HttpRunnerProcessor.objects.filter(name=teardown_method_name).filter(type=type)
        if len(search_post_code) > 0:
            # 后置代码已存在，数据进行更新
            HttpRunnerProcessor.objects.filter(name=teardown_method_name).filter(
                httprunner_id=id).filter(type=type).update(processor_code=post_processor_code)
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', teardown_method_name,
                                         search_post_code[0].processor_code, post_processor_code)
        else:
            httprunner_file_code_content(httprunner_project.name, '/debugtalk.py', teardown_method_name,
                                         post_processor_code)
            HttpRunnerProcessor.objects.create(
                name=teardown_method_name,
                type=type,
                processor_type='POST',
                processor_code=post_processor_code,
                httprunner_id=id
            )
        code_file = HTTP_RUNNER_PROJECT_DIR + httprunner_project.name + '/debugtalk.py'
        # 读取debugtalk中所有内容，并保存在数据库中
        with open(code_file, "r") as file:
            all_content = file.read()
        httprunner_project.code = all_content
        httprunner_project.save()


def env_code(httprunner_project_id, old_env_url, new_env_url):
    """
    环境内容处理
    @param: httprunner_project_id HttpRunner Project Id
    @param: old_env_url 原有的环境数据
    @param: new_env_url 新的环境数据
    """
    httprunner_project = get_object_or_404(HttpRunnerProjectInfo, id=httprunner_project_id)
    env_url_name = new_env_url.split('=')[0]
    httprunner_file_code_content(httprunner_project.name, '/.env', env_url_name, old_env_url, new_env_url)
    #  将处理完成的环境数据，更新code存储
    if len(httprunner_project.env_code) == 0:
        # 查询的环境信息不存在，则直接更新新的环境数据
        httprunner_project.env_code = new_env_url
    elif len(httprunner_project.env_code) != 0 and old_env_url in httprunner_project.env_code:
        # 查询的环境信息存在且则直接更新新的环境数据
        r_env_code = httprunner_project.env_code.replace(old_env_url, "").rstrip('\n')
        if len(r_env_code) == 0:
            new_env_code = new_env_url
        else:
            new_env_code = r_env_code + "\n" + new_env_url
        httprunner_project.env_code = new_env_code
    else:
        new_env_code = httprunner_project.env_code + "\n" + new_env_url
        httprunner_project.env_code = new_env_code
    httprunner_project.save()
