from django.db import models


# Create your models here.
class Project(models.Model):
    """
    项目管理表
    """
    name = models.CharField("名称", max_length=50, null=False)
    describe = models.TextField("描述", null=True, default="")
    image = models.CharField("图片", max_length=50, null=True)
    is_delete = models.BooleanField("状态", null=True, default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_project'
        verbose_name = '项目信息表'

    def __str__(self):
        """
        定义每个数据对象的显示信息
        """
        return self.name
