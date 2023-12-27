from typing import List

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from backend.common import response, Error
from backend.pagination import CustomPagination
from project.models import Project
from project.schema import ProjectIn, ProjectListOut, ProjectSearchIn

router = Router(tags=["projects"])


@router.post("/create")
@transaction.atomic
def create_project(request, data: ProjectIn):
    """
    创建项目
    """
    project = Project.objects.filter(name=data.name)
    if len(project) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)
    # 设置项目默认图片
    if data.image == "":
        data.image = "default_project_image.png"
    Project.objects.create(**data.dict())
    return response()


@router.post("/list", response=List[ProjectListOut])
@paginate(CustomPagination)
def project_list(request, data: ProjectSearchIn):
    """
    项目列表
    """
    # 构造查询条件
    query = Q() & Q(is_delete=False)
    if data.name:
        query &= Q(name__icontains=data.name)
    return Project.objects.filter(query).all()


@router.get("/{project_id}")
def project_detail(request, project_id: int):
    """
    获取项目详情
    """
    try:
        project = Project.objects.get(pk=project_id)
    except project.DoesNotExist:
        return response(error=Error.PROJECT_NOT_EXIST)
    else:
        if project.is_delete is True:
            return response(error=Error.PROJECT_IS_DELETE)
    data = {
        "id": project.id,
        "name": project.name,
        "describe": project.describe,
        "image": project.image,
        "create_time": project.create_time
    }
    return response(item=data)


@router.put("/{project_id}")
@transaction.atomic
def project_update(request, project_id: int, payload: ProjectIn):
    """
    更新项目详情
    """
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()
    return response()


@router.delete("/{project_id}")
@transaction.atomic
def project_delete(request, project_id: int):
    """
    项目删除
    """
    project = get_object_or_404(Project, id=project_id)
    project.is_delete = True
    project.save()
    return response()
