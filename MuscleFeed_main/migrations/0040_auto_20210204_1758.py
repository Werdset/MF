# Generated by Django 3.1.2 on 2021-02-04 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0039_auto_20210204_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='we_will_return',
        ),
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='we_will_return_he',
        ),
        migrations.RemoveField(
            model_name='accountpagesettings',
            name='we_will_return_ru',
        ),
    ]
