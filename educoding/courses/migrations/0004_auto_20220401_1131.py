# Generated by Django 2.2.12 on 2022-04-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20220401_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='comments',
            field=models.ManyToManyField(blank=True, to='courses.Comment'),
        ),
    ]
