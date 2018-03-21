# Generated by Django 2.0.2 on 2018-03-21 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chalkboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(max_length=500, verbose_name='Description')),
                ('is_private', models.BooleanField(default=0, verbose_name='Private')),
                ('is_active', models.BooleanField(default=1, verbose_name='Active')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('stickynote_create_own', 'Create own stickynotes'), ('stickynote_update_own', 'Update own stickynotes'), ('stickynote_delete_own', 'Delete own stickynotes'), ('stickynote_read_all', 'Read all stickynotes'), ('stickynote_update_all', 'Update all stickynotes'), ('stickynote_delete_all', 'Delete all stickynotes'), ('chalkboard_add_user', 'Add user to chalkboard'), ('chalkboard_remove_user', 'Remove user to chalkboard'), ('chalkboard_manage_permission_user', 'Manage permission user to chalkboard'), ('chalkboard_manage_permission', 'Manage permission chalkboard'), ('chalkboard_update', 'Update chalkboard'), ('chalkboard_delete', 'Delete chalkboard')),
            },
        ),
        migrations.CreateModel(
            name='FavoriteChalkboards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Chalkboard')),
            ],
        ),
        migrations.CreateModel(
            name='JoinChalkboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chalkboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Chalkboard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StickyNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text_content', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ImageStickyNote',
            fields=[
                ('stickynote_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notes.StickyNote')),
                ('image_content', models.URLField()),
            ],
            bases=('notes.stickynote',),
        ),
        migrations.CreateModel(
            name='VideoStickyNote',
            fields=[
                ('stickynote_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notes.StickyNote')),
                ('video_content', embed_video.fields.EmbedVideoField()),
            ],
            bases=('notes.stickynote',),
        ),
        migrations.AddField(
            model_name='stickynote',
            name='chalkboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Chalkboard'),
        ),
        migrations.AddField(
            model_name='stickynote',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
