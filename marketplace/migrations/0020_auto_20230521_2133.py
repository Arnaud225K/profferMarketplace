# Generated by Django 3.2.9 on 2023-05-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0019_auto_20230521_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='section',
        ),
        migrations.AddField(
            model_name='product',
            name='section',
            field=models.ManyToManyField(blank=True, null=True, related_name='section_products', to='marketplace.Section'),
        ),
    ]
