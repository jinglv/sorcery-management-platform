from django.db import models

from modules.models import Module
from project.models import Project


class CasesSuite(models.Model):
    """
    测试用例集
    """
    name = models.CharField("名称", max_length=50, null=False)
    version_number = models.CharField("版本version_number", null=False, max_length=200, default="")
    case_ids = models.CharField("关联用例id", max_length=200, null=True, default=0)
    status = models.CharField("状态 0-未执行 1-执行中 2-已执行", max_length=10, null=True, default=0)
    describe = models.TextField("描述", null=True, default="")
    is_delete = models.BooleanField("是否删除", null=True, default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_cases_suite'
        verbose_name = '测试用例集'

    def __str__(self):
        return self.name


class TestCase(models.Model):
    """
    测试用例表
    关联 版本信息 接口信息
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version_number = models.CharField("版本id集合", null=False, max_length=200)
    name = models.CharField("测试用例名称", max_length=50, null=False)
    type = models.IntegerField("测试类型：1-功能测试，2-接口测试", null=False)
    test_label = models.IntegerField("测试标签：1-正向场景测试用例，2-异常场景测试用例", null=False)
    importance = models.IntegerField("重要程度：1-P0，2-P1，3-P2，4-P3", null=False)
    priority = models.IntegerField("优先级：1-高，2-中，3-低", null=True, default=0)
    precondition = models.TextField("前置条件", null=True, default="")
    test_steps = models.CharField("关联测试步骤集", max_length=200, null=False)
    result_status = models.IntegerField("执行结果：1-失败，2-通过", null=True, default=0)
    bug_list = models.CharField("Bug列表", max_length=200, null=True, default="")
    remark = models.TextField("备注", null=True, default="")
    is_delete = models.BooleanField("是否删除", null=True, default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_test_case'
        verbose_name = '测试用例表'

    def __str__(self):
        return self.name


class TestStep(models.Model):
    """
    测试步骤集
    """
    name = models.CharField("测试用例名称", max_length=50, null=False)
    test_step = models.CharField("测试步骤", max_length=255, null=False)
    test_data = models.CharField("测试数据", max_length=255, null=False)
    expected_result = models.CharField("预期结果", max_length=255, null=False)
    actual_result = models.CharField("实际结果", max_length=255, null=True, default="")
    step_status = models.IntegerField("测试步骤执行测试结果：1-未通过 2-通过", null=True, default=0)
    api_id = models.IntegerField("接口id", null=True, default=0)
    remark = models.TextField("备注", null=True, default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_test_step'
        verbose_name = '测试步骤集'

    def __str__(self):
        return self.name


class VersionInfo(models.Model):
    """
    版本信息
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("需求名称", max_length=50, null=False)
    version_number = models.CharField("版本号", max_length=50, null=False)
    requirements_type = models.CharField("需求类型：业务类需求/Bug改进需求/技术类需求", max_length=20, null=False)
    requirements = models.TextField("该版本的需求文本/链接/文件/图片", null=True, default="")
    requirements_upload_file = models.TextField("需求上传的文件/图片-列表", null=True, default="")
    demand_analysis = models.TextField("需求分析/链接/文本/图片/视频", null=True, default="")
    describe = models.TextField("版本说明", null=True, default="")
    is_delete = models.BooleanField("是否删除", null=True, default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_test_version_info'
        verbose_name = '版本信息表'

    def __str__(self):
        return self.version_number
