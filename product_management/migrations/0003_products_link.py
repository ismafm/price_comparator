# Generated by Django 4.1.7 on 2023-06-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0002_products_delete_theodoteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='link',
            field=models.CharField(default=None, max_length=1000, unique=True),
        ),
    ]