from django.db import models

from modules.models import Module
from project.models import Project


class ApiInfo(models.Model):
    """
    接口信息
    """
    # 测试用例和模块关联
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    api_path = models.TextField("接口请求地址", null=False)
    method = models.CharField("请求方法", max_length=10, null=False)  # GET/POST/DELETE/PUT
    header = models.TextField("请求头", null=True, default="{}")
    params_type = models.CharField("参数类型", max_length=10, null=False)  # GET: params POST: form/json
    params_body = models.TextField("参数内容", null=True, default="{}")
    response = models.TextField("响应", null=True, default="{}")
    is_delete = models.BooleanField("状态", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_api_info'
        verbose_name = '项目信息表'

    def __str__(self):
        return self.name


class ApiExtract(models.Model):
    """
    提取器保存表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    apis_id = models.IntegerField("接口ID", null=False, default=0)
    name = models.CharField("名称", max_length=50, null=False)
    extract = models.CharField("提取规则", max_length=200, null=False)
    value = models.CharField("提取值", max_length=200, null=True, default="")
    # type = models.IntegerField("提取器变量类型：1-提取变量，2-环境变量", null=False, default=1)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_api_extract'
        verbose_name = '提取器保存表'

    def __str__(self):
        return self.name


class ApiAssert(models.Model):
    """
    断言信息保存表
    """
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    assert_type = models.CharField("断言类型", max_length=10, null=True)  # include/equal
    assert_extract = models.TextField("断言提取表达式", null=True, default="")
    expect_text = models.TextField("预期值", null=True, default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_api_assert'
        verbose_name = '断言信息保存表'

    def __str__(self):
        return self.name
