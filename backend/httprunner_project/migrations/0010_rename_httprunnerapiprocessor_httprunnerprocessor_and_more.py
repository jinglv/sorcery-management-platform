# Generated by Django 4.2.2 on 2023-07-08 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('httprunner_project', '0009_httprunnerapiprocessor_processor_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HttpRunnerApiProcessor',
            new_name='HttpRunnerProcessor',
        ),
        migrations.AlterModelTable(
            name='httprunnerprocessor',
            table='t_httprunner_processor',
        ),
        migrations.CreateModel(
            name='HttpRunnerTestCaseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='api名称')),
                ('httpruuner_api_ids', models.IntegerField(default=[], verbose_name='关联HttpRunner接口ID集')),
                ('config_content', models.TextField(default='', null=True, verbose_name='HttpRunner TestCase配置信息')),
                ('test_case_info', models.TextField(default='{}', null=True, verbose_name='HttpRunner TestCase信息')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('httprunner_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='httprunner_project.httprunnerprojectinfo')),
            ],
            options={
                'verbose_name': 'HttpRunner测试用例信息表',
                'db_table': 't_httprunner_test_case_info',
            },
        ),
    ]
