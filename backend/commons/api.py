# Create your views here.
import hashlib
import os

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile, File

from backend.common import response, Error
from backend.settings import IMAGE_DIR, FILE_DIR
from httprunner_project.models import HttpRunnerProjectInfo, HttpRunnerApiInfo, HttpRunnerTestCaseInfo, \
    HttpRunnerSuiteInfo
from project.models import Project

router = Router(tags=["commons"])


@router.post("/upload")
@transaction.atomic
def project_image_upload(request, file: UploadedFile = File(...)):
    """
    项目图片上传
    """
    # 判断文件后缀名
    suffix = file.name.split(".")[-1]
    if suffix not in ["png", "jpg", "jpeg", "gif"]:
        return response(error=Error.IMAGE_SUFFIX_ERROR)

    # 判断文件大小 1024 * 1024 * 2 = 2MB
    if file.size > 2097152:
        return response(error=Error.IMAGE_SIZE_ERROR)

    # 文件名生成md5
    file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
    file_name = file_md5 + "." + suffix

    # 保存到本地
    upload_file = os.path.join(IMAGE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    upload_file_info = {
        "name": file_name
    }
    return response(item=upload_file_info)


@router.post("/file")
@transaction.atomic
def file_upload(request, file: UploadedFile = File(...)):
    """
    文件上传
    """
    # 判断文件后缀名
    # suffix = file.name.split(".")[-1]

    # 判断文件大小 1024 * 1024 * 2 = 2MB
    if file.size > 2097152:
        return response(error=Error.IMAGE_SIZE_ERROR)

    # 文件名生成md5
    # file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
    # file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "." + suffix
    file_name = file.name

    # 保存到本地
    upload_file = os.path.join(FILE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    upload_file_info = {
        "name": file_name
    }
    return response(item=upload_file_info)


@router.post("/editor/file/{type}")
@transaction.atomic
def editor_file_upload(request, type: str, file: UploadedFile = File(...)):
    """
    富文本框 --文件上传 兼容组件需求的数据格式，上传接口返回的格式必须是：
    {
     "errno": 0,
     "data": [
            {
                "url": ""
            }
        ]
    }
    """
    # 判断文件大小 1024 * 1024 * 50 = 50MB
    if file.size > 52428800:
        return response(error=Error.IMAGE_SIZE_ERROR)
    file_name = file.name

    print('ip -> ', request.get_host())
    # 保存到本地
    upload_file = os.path.join(FILE_DIR, file_name)
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    if type == 'image':
        upload_file_info = {
            "errno": 0,
            "data": [
                {
                    "url": 'http://' + request.get_host() + "/static/file/" + file_name
                }
            ]
        }
    elif type == 'video':
        upload_file_info = {
            "errno": 0,
            "data": {
                "url": 'http://' + request.get_host() + "/static/file/" + file_name
            }
        }
    else:
        upload_file_info = {"errno": 0}
    return upload_file_info


@router.get("/statistics/hr")
def statistics_http_runner_data(request):
    """
    统计数据：
    HttpRunner项目 - 接口总数、用例总数、测试套件总数
    [{
        "project_name": 项目名称,
        "apis_count": 接口总数,
        "test_cases_count": 测试用例总数,
        "test_suite_count": 测试套件总数
    }]
    """
    count_list = []
    # 1.查询HttpRunner项目
    http_runner_project_info = HttpRunnerProjectInfo.objects.all()
    # 2.遍历查询项目信息，根据项目id，查询接口总数、测试用例总数、测试套件总数
    for project_info in http_runner_project_info:
        project = get_object_or_404(Project, pk=project_info.project_id)
        # 查询接口总数
        apis_count = HttpRunnerApiInfo.objects.filter(httprunner_project_id=project_info.id).count()
        # 查询测试用例总数
        test_cases_count = HttpRunnerTestCaseInfo.objects.filter(httprunner_project_id=project_info.id).count()
        # 查询测试套件总数
        test_suite_count = HttpRunnerSuiteInfo.objects.filter(httprunner_project_id=project_info.id).count()
        count_info = {
            "project_name": project.name,
            "apis_count": apis_count,
            "test_cases_count": test_cases_count,
            "test_suite_count": test_suite_count
        }
        count_list.append(count_info)
    return response(item=count_list)


@router.get("/statistics/hr/total")
def statistics_http_runner_total_data(request):
    """
    查询HttpRunner项目总数
    [{
        "project_total": 项目总数,
        "apis_total": 接口总数,
        "test_cases_total": 测试用例总数,
        "test_suite_total": 测试套件总数
    }]
    """
    # 查询项目总数
    project_total = HttpRunnerProjectInfo.objects.count()
    # 查询接口总数
    apis_total = HttpRunnerApiInfo.objects.count()
    # 查询测试用例总数
    test_cases_total = HttpRunnerTestCaseInfo.objects.count()
    # 查询测试套件总数
    test_suite_total = HttpRunnerSuiteInfo.objects.count()
    total_info = {
        "project_total": project_total,
        "apis_total": apis_total,
        "test_cases_total": test_cases_total,
        "test_suite_total": test_suite_total
    }
    return response(item=total_info)
