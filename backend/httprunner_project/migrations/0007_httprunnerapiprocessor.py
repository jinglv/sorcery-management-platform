# Generated by Django 4.2.2 on 2023-06-29 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('httprunner_project', '0006_alter_httprunnerapiinfo_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HttpRunnerApiProcessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='方法名称')),
                ('type', models.CharField(default='', max_length=50, verbose_name='类型(Api、TestCase、TestSuite)')),
                ('pre_processor', models.TextField(default='', null=True, verbose_name='前置处理器')),
                ('post_processor', models.TextField(default='', null=True, verbose_name='后置处理器')),
                ('httprunner_api_id', models.IntegerField(default=0, null=True, verbose_name='关联接口ID')),
                ('httprunner_case_id', models.IntegerField(default=0, null=True, verbose_name='关联用例ID')),
                ('httprunner_suite_id', models.IntegerField(default=0, null=True, verbose_name='关联用例集ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'HttpRunner hook存储表',
                'db_table': 't_httprunner_api_processor',
            },
        ),
    ]