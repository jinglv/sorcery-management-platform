from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.
from ninja import Router
from ninja.pagination import paginate

from backend.common import response, model_to_dict, Error
from backend.pagination import CustomPagination
from envs.models import Envs
from envs.schema import EnvIn, EnvListOut, EnvSearchIn
from project.models import Project

router = Router(tags=["env"])


@router.post('/create')
def create_env(request, env: EnvIn):
    """
    创建环境信息
    """
    get_object_or_404(Project, pk=env.project_id)
    env_obj = Envs.objects.create(
        name=env.name,
        project_id=env.project_id,
        env=env.env,
        browser=env.browser,
        protocol=env.protocol,
        base_url=env.base_url)
    return response(item=model_to_dict(env_obj))


@router.get('/detail/{env_id}')
def get_env(request, env_id: int):
    """
    获取环境环境详情
    """
    try:
        env = Envs.objects.get(id=env_id)
        project = get_object_or_404(Project, pk=env.project_id, is_delete=False)
        project_name = project.name
        env_dict = {
            'id': env.id,
            'name': env.name,
            'project_id': env.project_id,
            'project_name': project_name,
            'env': env.env,
            'browser': env.browser,
            'base_url': env.base_url,
            'protocol': env.protocol,
            'create_time': env.create_time,
            'update_time': env.update_time
        }
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)
    return response(item=env_dict)


@router.put('/update/{env_id}')
def update_env(request, env_id: int, env: EnvIn):
    """
    更新环境信息
    """
    try:
        env_obj = Envs.objects.get(id=env_id)
        env_obj.name = env.name
        env_obj.project_id = env.project_id
        env_obj.env = env.env
        env_obj.browser = env.browser
        env_obj.base_url = env.base_url
        env_obj.protocol = env.protocol
        env_obj.save()
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)
    return response()


@router.post('/list', response=List[EnvListOut])
@paginate(CustomPagination)
def get_env_list(request, env: EnvSearchIn):
    """
    获取所有环境列表
    """
    # 构建查询条件
    query = Q()
    if env.name:
        query &= Q(name__icontains=env.name)
    if env.project_id:
        query &= Q(project_id=env.project_id)
    if env.env:
        query &= Q(env__icontains=env.env)
    if env.browser:
        query &= Q(browser__icontains=env.browser)
    if env.protocol:
        query &= Q(protocol__icontains=env.protocol)
    if env.base_url:
        query &= Q(base_url__icontains=env.base_url)

    envs = Envs.objects.filter(query)
    result = []
    for env in envs:
        print('env:', env)
        # 查询项目是否存在
        project = get_object_or_404(Project, pk=env.project_id, is_delete=False)
        project_name = project.name
        env_dict = {
            'id': env.id,
            'name': env.name,
            'project_id': env.project_id,
            'project_name': project_name,
            'env': env.env,
            'browser': env.browser,
            'base_url': env.base_url,
            'protocol': env.protocol,
            'create_time': env.create_time,
            'update_time': env.update_time
        }
        result.append(env_dict)
    return result


@router.get('/{project_id}/list')
def get_env_list_for_project(request, project_id: int):
    """
    获取环境信息列表
    """
    envs = Envs.objects.filter(project_id=project_id).all()
    env_list = []
    for env in envs:
        env_list.append(model_to_dict(env))
    return response(item=env_list)


@router.delete('/{env_id}')
def delete_env(request, env_id: int):
    """
    删除环境信息
    """
    try:
        env = Envs.objects.get(id=env_id)
        env.delete()
    except Envs.DoesNotExist:
        return response(error=Error.ENV_IS_NULL)
    return response()
