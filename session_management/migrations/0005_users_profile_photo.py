# Generated by Django 4.1.7 on 2023-06-02 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_management', '0004_remove_users_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='profile_photo',
            field=models.CharField(default='img/profile_photos/none.jpg', max_length=100),
        ),
    ]
