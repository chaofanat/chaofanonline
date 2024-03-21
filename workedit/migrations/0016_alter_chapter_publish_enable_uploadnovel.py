# Generated by Django 5.0.1 on 2024-03-20 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workedit', '0015_chapter_publish_enable_novel_publish_enable_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='publish_enable',
            field=models.BooleanField(default=False, verbose_name='是否发布'),
        ),
        migrations.CreateModel(
            name='Uploadnovel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=200, null=True)),
                ('file_path', models.CharField(max_length=200, null=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('enable', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['create_time'],
            },
        ),
    ]