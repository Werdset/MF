# Generated by Django 3.1.2 on 2020-12-22 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0019_auto_20201221_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(default=1, verbose_name='Порядковый номер'),
            preserve_default=False,
        ),
    ]
