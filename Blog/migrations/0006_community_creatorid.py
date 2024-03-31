# Generated by Django 4.2.11 on 2024-03-31 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0005_alter_community_numberofmembers'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='CreatorId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
