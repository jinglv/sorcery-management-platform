# Generated by Django 4.2.2 on 2023-06-19 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('envs', '0003_rename_project_id_envs_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='envs',
            options={'verbose_name': '版本信息表'},
        ),
        migrations.AlterModelTable(
            name='envs',
            table='t_envs',
        ),
    ]
