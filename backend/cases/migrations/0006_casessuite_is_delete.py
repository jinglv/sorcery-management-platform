# Generated by Django 4.2.2 on 2023-12-13 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0005_remove_testcase_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="casessuite",
            name="is_delete",
            field=models.BooleanField(default=False, null=True, verbose_name="是否删除"),
        ),
    ]
