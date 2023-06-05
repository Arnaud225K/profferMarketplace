# Generated by Django 3.2.9 on 2023-04-07 06:04

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0005_alter_subcategory_subcategory_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'sections',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(upload_to='media/product')),
                ('product_name', models.CharField(max_length=255, unique=True)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('product_information', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('model_name', models.CharField(max_length=255)),
                ('tags', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('is_available', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=500, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='marketplace.section')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'products',
            },
        ),
    ]
