# Create your views here.
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.params import Query

from backend.common import response, Error, model_to_dict
from backend.tree_helper import module_tree
from modules.models import Module
from modules.schema import ModuleIn, ProjectIn
from project.models import Project

router = Router(tags=["modules"])


@router.post("/create")
@transaction.atomic
def create_module(request, data: ModuleIn):
    """
    创建项目
    """
    # 查询项目是否存在
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)
    # 查询项目下的模块名称是否存在
    module = Module.objects.filter(name=data.name, project_id=data.project_id)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)

    module = Module.objects.create(**data.dict())
    return response(item=model_to_dict(module))


@router.get("/tree")
def get_module_tree(request, filters: ProjectIn = Query(...)):
    """
    获取模块树
    """
    # 获取指定项目下的所有模块
    modules = Module.objects.filter(project_id=filters.project_id, is_delete=False)
    data_node = []
    for m in modules:
        data_node.append({
            "id": m.id,
            "parent_id": m.parent_id,
            "label": m.name,
            "children": [],
        })
    data = module_tree(data_node)
    return response(item=data)


@router.delete("/{module_id}/")
@transaction.atomic
def module_delete(request, module_id: int):
    """
    模块删除
    """
    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()
    return response()
