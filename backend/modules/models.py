from django.db import models

# Create your models here.
from project.models import Project


class Module(models.Model):
    """
    模块(节点)表
    """
    #  模块与项目关联
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False, default="")
    parent_id = models.IntegerField("父级ID", default=0)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_module'
        verbose_name = '模块信息表'

    def __str__(self):
        return self.name
