# Generated by Django 4.1.7 on 2023-05-23 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('envs', '0002_rename_project_envs_project_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='envs',
            old_name='project_id',
            new_name='project',
        ),
    ]
