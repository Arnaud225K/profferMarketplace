# Generated by Django 3.2.9 on 2023-06-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0026_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, unique=True),
        ),
    ]
