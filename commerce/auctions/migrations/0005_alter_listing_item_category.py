# Generated by Django 4.2.1 on 2023-05-22 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='item_category',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
