# Generated by Django 2.2.12 on 2022-04-01 13:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20220401_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sector',
            name='sectorLoadedIMG',
        ),
        migrations.AddField(
            model_name='sector',
            name='sector_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='sector_image'),
            preserve_default=False,
        ),
    ]
