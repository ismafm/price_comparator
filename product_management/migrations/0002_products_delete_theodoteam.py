# Generated by Django 4.1.7 on 2023-06-03 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000, unique=True)),
                ('price', models.FloatField(null=True)),
                ('photo', models.CharField(max_length=100, unique=True)),
                ('logo', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TheodoTeam',
        ),
    ]
