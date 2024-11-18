# Generated by Django 5.1.1 on 2024-11-17 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.CharField(max_length=50, unique=True)),
                ('text', models.TextField()),
                ('author_name', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField()),
                ('like_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('view_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_id', models.CharField(max_length=255, unique=True)),
                ('author', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('like_count', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='youtube.comment')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='youtube.video'),
        ),
    ]
