# Generated by Django 4.1.7 on 2023-06-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_management', '0005_users_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='user2',
            field=models.CharField(default='aaa', max_length=18, unique=True),
        ),
    ]
