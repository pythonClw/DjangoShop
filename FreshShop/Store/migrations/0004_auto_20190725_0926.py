# Generated by Django 2.1.8 on 2019-07-25 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_goods_good_under'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='good_under',
            new_name='goods_under',
        ),
    ]
