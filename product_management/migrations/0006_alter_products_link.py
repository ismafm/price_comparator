# Generated by Django 4.1.7 on 2023-06-03 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0005_products_fk_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='link',
            field=models.CharField(default=None, max_length=3000),
        ),
    ]