# Generated by Django 3.2.9 on 2023-05-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0020_auto_20230521_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='section',
            field=models.ManyToManyField(blank=True, related_name='section_products', to='marketplace.Section'),
        ),
    ]