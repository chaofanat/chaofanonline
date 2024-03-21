# Generated by Django 5.0.1 on 2024-02-25 13:28

import django.db.models.deletion
import markdownx.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workedit', '0008_alter_chapter_options_alter_chapter_content_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=markdownx.models.MarkdownxField(default='此处是正文。。。。从前有座山，山里有座庙。。。。（支持markdown语法哦）', verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(default='这章叫什么好呢？', max_length=100, verbose_name='章节名'),
        ),
        migrations.AlterField(
            model_name='novel',
            name='title',
            field=models.CharField(default='取一个高端大气的小说名吧', max_length=100, verbose_name='作品名 '),
        ),
        migrations.CreateModel(
            name='Aiapikey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key_name', models.CharField(max_length=20)),
                ('key', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Aichatsession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_title', models.CharField(max_length=20)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Aichatcontent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=10)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workedit.aichatsession')),
            ],
            options={
                'ordering': ['create_time'],
            },
        ),
    ]