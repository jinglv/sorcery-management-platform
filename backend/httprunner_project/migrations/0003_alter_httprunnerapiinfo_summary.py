# Generated by Django 4.2.2 on 2023-06-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('httprunner_project', '0002_httprunnerapiinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='httprunnerapiinfo',
            name='summary',
            field=models.TextField(default='', null=True, verbose_name='测试运行结果信息'),
        ),
    ]
