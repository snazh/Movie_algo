# Generated by Django 5.0.3 on 2024-03-05 03:18

import django.db.models.deletion
import users_management.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=users_management.models.user_avatar_upload_to)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
