# Generated by Django 2.0.2 on 2018-02-27 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20180227_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stickynote',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='stickynote',
            old_name='user_created_id',
            new_name='user_created',
        ),
    ]
