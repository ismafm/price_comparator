# Generated by Django 4.1.7 on 2023-06-02 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session_management', '0006_users_user2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user2',
        ),
    ]
