# Generated by Django 5.1.1 on 2024-10-15 05:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='likes',
        ),
        migrations.AddField(
            model_name='photo',
            name='likes_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='contest.photo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'photo')},
            },
        ),
    ]
