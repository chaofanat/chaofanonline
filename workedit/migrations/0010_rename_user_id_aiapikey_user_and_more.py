# Generated by Django 5.0.1 on 2024-02-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workedit', '0009_alter_chapter_content_alter_chapter_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aiapikey',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='aichatcontent',
            old_name='session_id',
            new_name='session',
        ),
        migrations.RenameField(
            model_name='aichatsession',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='aichatsession',
            name='session_title',
            field=models.CharField(default='默认标题', max_length=20),
        ),
    ]
