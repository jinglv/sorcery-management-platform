from django.db import models


# Create your models here.
class Infos(models.Model):
    """
    解析后的接口信息保存
    """
    name = models.CharField("文件名称", max_length=255, null=False)
    url = models.CharField("接口地址", max_length=255, null=False)
    method = models.CharField("请求方法", max_length=10, null=False)  # GET/POST/DELETE/PUT
    request_headers = models.TextField("请求头信息", null=True, default="[]")
    request_params = models.TextField("请求参数param", null=True, default="[]")
    request_body = models.TextField("参数内容", null=True, default="{}")
    response_body = models.TextField("响应", null=True, default="{}")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 't_tripartite_api_info'
        verbose_name = '解析接口信息表'

    def __str__(self):
        return self.name
