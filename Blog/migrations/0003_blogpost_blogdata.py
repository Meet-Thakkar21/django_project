# Generated by Django 4.2.11 on 2024-03-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_blogger_userid_alter_blogpost_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='BlogData',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
