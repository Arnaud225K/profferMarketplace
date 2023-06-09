# Generated by Django 3.2.9 on 2023-05-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0007_alter_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='district',
            field=models.CharField(choices=[('Верх-Исетский район', 'Верх-Исетский район'), ('Железнодорожный район', 'Железнодорожный район'), ('Кировский район', 'Кировский район'), ('Ленинский район', 'Ленинский район'), ('Лесное кладбище', 'Лесное кладбище'), ('Октябрьский район', 'Октябрьский район'), ('Орджоникидзевский район', 'Орджоникидзевский район'), ('Чкаловский район', 'Чкаловский район'), ('микрорайон ЖБИ', 'микрорайон ЖБИ')], max_length=100, null=True),
        ),
    ]
