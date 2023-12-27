from django.db import models

# Create your models here.
from project.models import Project


class HttpRunnerProjectInfo(models.Model):
    """
    httpRunner项目信息表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("httpRunner项目名称", max_length=50, null=False)
    describe = models.TextField("描述", null=True, default="")
    code = models.TextField("httpRunner debugTalk执行代码", null=True, default="")
    env_code = models.TextField("httpRunner .env环境变量", null=True, default="")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_project'
        verbose_name = 'HttpRunner项目信息表'

    def __str__(self):
        return self.name


class HttpRunnerApiInfo(models.Model):
    """
    httpRunner接口信息表(将基础接口信息转为HttpRunner需求格式)
    """
    httprunner_project = models.ForeignKey(HttpRunnerProjectInfo, on_delete=models.CASCADE)
    name = models.CharField("api名称", max_length=50, null=False)
    api_id = models.IntegerField("关联接口ID", null=False, default=0)
    api_info = models.TextField("接口信息", null=True, default="{}")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_api_info'
        verbose_name = 'HttpRunner接口信息表'

    def __str__(self):
        return self.name


class HttpRunnerRunInfo(models.Model):
    """
    HttpRunner执行
    """
    name = models.CharField("执行名称，当前时间指定格式", max_length=50, null=False)
    ids = models.CharField("执行列表", max_length=200, null=False, default=[])
    type = models.CharField("类型(Api、TestCase、TestSuite)", max_length=50, null=False, default="")
    summary = models.TextField("测试运行结果信息", null=True, default="")
    result = models.TextField("运行结果（non-未执行 fail-失败 error-错误 success-成功）", null=True, default="")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_run_info'
        verbose_name = 'HttpRunner执行结果信息表'

    def __str__(self):
        return self.name


class HttpRunnerProcessor(models.Model):
    """
    HttpRunner hook存储表
    """
    name = models.CharField("方法名称", max_length=50, null=False)
    type = models.CharField("类型(Api、TestCase、TestSuite)", max_length=50, null=False, default="")
    processor_type = models.CharField("处理器代码类型（PRE-前置，POST-后置）", max_length=50, null=False, default="")
    processor_code = models.TextField("代码", null=True, default="")
    httprunner_id = models.IntegerField("关联接口/用例/用例集ID", null=True, default=0)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_processor'
        verbose_name = 'HttpRunner hook存储表'

    def __str__(self):
        return self.name


class HttpRunnerTestCaseInfo(models.Model):
    """
    httpRunner测试用例信息表
    """
    httprunner_project = models.ForeignKey(HttpRunnerProjectInfo, on_delete=models.CASCADE)
    name = models.CharField("测试用例名称", max_length=50, null=False)
    config_content = models.TextField("HttpRunner TestCase配置信息", null=True, default="")
    test_case_info = models.TextField("HttpRunner TestCase信息", null=True, default="{}")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_test_case_info'
        verbose_name = 'HttpRunner测试用例信息表'

    def __str__(self):
        return self.name


class HttpRunnerSuiteInfo(models.Model):
    """
    httpRunner测试用例集信息表
    """
    httprunner_project = models.ForeignKey(HttpRunnerProjectInfo, on_delete=models.CASCADE)
    name = models.CharField("测试用例集名称", max_length=50, null=False)
    config_content = models.TextField("HttpRunner TestCase配置信息", null=True, default="")
    suite_info = models.TextField("HttpRunner TestCase信息", null=True, default="{}")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = 't_httprunner_suite_info'
        verbose_name = 'HttpRunner测试用例集信息表'

    def __str__(self):
        return self.name
