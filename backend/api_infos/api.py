import json
import os
from typing import List

from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from api_infos.har_utils import api_info
from api_infos.models import Infos
from api_infos.schema import HarFileIn, InfosIn, InfosOut, YapiBaseIn, YapiIn, YapiCategoryApiIn, YapiApiDetailsIn
from api_infos.utils import z_request, get_response_data
from api_infos.yapi_parser import data_parser
from backend.common import response, Error
from backend.pagination import CustomPagination
from backend.settings import FILE_DIR

router = Router(tags=["info"])


@router.post("/har")
def har_api_info(request, data: HarFileIn):
    """
    上传har文件解析接口信息
    """
    if data.har_file is None:
        return response(error=Error.HAR_FILE_IS_ERROR)
    # 读取上传的har文件
    har_file_path = FILE_DIR + '/' + data.har_file
    api_info_list = api_info(har_file_path)
    return response(item=api_info_list)


@router.get("/har-file-list")
def har_file_list(request):
    """
    获取上传har文件列表
    """
    # 读取上传har文件本地文件夹
    file_list = os.listdir(FILE_DIR)
    file_info_list = []
    for i in file_list:
        suffix = i.split(".")[-1]
        if suffix == 'har':
            file_info = {
                "file_name": i
            }
            file_info_list.append(file_info)
    return response(item=file_info_list)


@router.post("/save")
@transaction.atomic
def save_infos(request, data: InfosIn):
    """
    保存解析接口信息
    """
    Infos.objects.create(**data.dict())
    return response()


@router.get("/list/{file_name}", response=List[InfosOut])
@paginate(CustomPagination)
def infos_list(request, file_name: str, **kwargs):
    """
    接口信息列表
    """
    results = []
    infos = list(Infos.objects.filter(name=file_name).values())
    for info in infos:
        result = {
            'id': info.get('id'),
            'name': info.get('name'),
            'url': info.get('url'),
            'method': info.get('method'),
            'request_headers': json.loads(info.get('request_headers').replace('\'', '"')),
            'request_params': json.loads(info.get('request_params').replace('\'', '"')),
            'request_body': json.loads(info.get('request_body').replace('\'', '"')),
            'response_body': json.loads(info.get('response_body')),
            'create_time': info.get('create_time')
        }
        results.append(result)
    return results


@router.get("/{api_info_id}")
def api_info_detail(request, api_info_id: int):
    """
    获取解析接口详情
    """
    info = get_object_or_404(Infos, id=api_info_id)
    result = {
        'id': info.id,
        'name': info.name,
        'url': info.url,
        'method': info.method,
        'request_headers': json.loads(info.request_headers.replace('\'', '"')),
        'request_params': json.loads(info.request_params.replace('\'', '"')),
        'request_body': json.loads(info.request_body.replace('\'', '"')),
        'response_body': json.loads(info.response_body),
        'create_time': info.create_time
    }
    return response(item=result)


@router.post("/yapi/project/info")
def get_yapi_project_info(request, data: YapiBaseIn):
    """
    根据yapi基础信息获取项目信息
    """
    param = {'token': data.yapi_token}
    response_data = z_request(data.yapi_base_url, '/api/project/get', param).json()
    yapi_project_info = {
        "project_id": get_response_data(response_data, '$.data._id')[0],
        "project_name": get_response_data(response_data, '$.data.name')[0]
    }
    return response(item=yapi_project_info)


@router.post("/yapi/category/list")
def get_yapi_category_list(request, data: YapiIn):
    """
    根据项目id获取项目下的分类信息
    """
    category_info_list = []
    param = {
        'project_id': data.project_id,
        'token': data.yapi_token
    }
    response_data = z_request(data.yapi_base_url, '/api/interface/getCatMenu', param).json()
    data_list = get_response_data(response_data, '$.data[*]')
    for data in data_list:
        category_info = {
            'category_id': data['_id'],
            'category_name': data['name']
        }
        category_info_list.append(category_info)
    return response(item=category_info_list)


@router.post("/yapi/api/list")
def get_yapi_category_api_list(request, data: YapiCategoryApiIn):
    """
    获取分类下的接口信息
    """
    param = {
        'catid': data.category_id,
        'token': data.yapi_token,
        'page': data.page,
        'limit': data.size
    }
    response_data = z_request(data.yapi_base_url, '/api/interface/list_cat', param).json()
    total = get_response_data(response_data, '$.data.total')[0]
    count = get_response_data(response_data, '$.data.count')[0]
    resp_api_list = get_response_data(response_data, '$.data.list[*]')
    result_list = []
    if resp_api_list is False:
        return response(item=result_list)
    for api in resp_api_list:
        result = {
            'project_id': api['project_id'],
            'category_id': api['catid'],
            'api_id': api['_id'],
            'api_name': api['title'],
            'api_path': api['path']
        }
        result_list.append(result)
    result = {
        'count': count,
        'total': total,
        'list': result_list
    }
    return response(item=result)


@router.post("/yapi/api/detail")
def yapi_api_detail(request, data: YapiApiDetailsIn):
    """
    获取接口详情
    """
    param = {
        'token': data.yapi_token,
        'id': data.api_id
    }
    response_data = z_request(data.yapi_base_url, '/api/interface/get', param).json()
    resp_data = response_data['data']
    return response(item=data_parser(resp_data))
