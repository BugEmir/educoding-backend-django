# Generated by Django 2.2.12 on 2022-04-01 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20220401_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='courseUUID',
            new_name='course_uuid',
        ),
    ]
