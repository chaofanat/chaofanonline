# Generated by Django 5.0.1 on 2024-03-20 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workedit', '0016_alter_chapter_publish_enable_uploadnovel'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadnovel',
            name='check_result',
            field=models.CharField(max_length=200, null=True),
        ),
    ]