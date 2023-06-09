# Generated by Django 4.0.6 on 2022-07-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default/person.jpeg', null=True, upload_to='photo/%Y/%m/%d/'),
        ),
    ]
