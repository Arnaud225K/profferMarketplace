# Generated by Django 3.2.9 on 2023-04-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]