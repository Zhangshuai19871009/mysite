# Generated by Django 2.0.6 on 2018-06-08 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0003_auto_20180608_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likecount',
            old_name='liked_num',
            new_name='liked_nums',
        ),
    ]
