# Generated by Django 4.0.6 on 2022-07-08 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_statud_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(max_length=10, null=True),
        ),
    ]