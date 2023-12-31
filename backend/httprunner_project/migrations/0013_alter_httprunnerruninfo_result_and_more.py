# Generated by Django 4.2.2 on 2023-07-19 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('httprunner_project', '0012_remove_httprunnerprocessor_httprunner_api_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='httprunnerruninfo',
            name='result',
            field=models.TextField(default='', null=True, verbose_name='运行结果（non-未执行 fail-失败 error-错误 success-成功）'),
        ),
        migrations.AlterField(
            model_name='httprunnertestcaseinfo',
            name='name',
            field=models.CharField(max_length=50, verbose_name='测试用例名称'),
        ),
        migrations.CreateModel(
            name='HttpRunnerSuiteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='测试用例集名称')),
                ('config_content', models.TextField(default='', null=True, verbose_name='HttpRunner TestCase配置信息')),
                ('suite_info', models.TextField(default='{}', null=True, verbose_name='HttpRunner TestCase信息')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('httprunner_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='httprunner_project.httprunnerprojectinfo')),
            ],
            options={
                'verbose_name': 'HttpRunner测试用例集信息表',
                'db_table': 't_httprunner_suite_info',
            },
        ),
    ]
