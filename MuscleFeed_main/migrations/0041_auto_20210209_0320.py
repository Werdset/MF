# Generated by Django 3.1.2 on 2021-02-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0040_auto_20210204_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='freezes',
            field=models.ManyToManyField(blank=True, null=True, to='MuscleFeed_main.OrderFreeze', verbose_name='Заморозки'),
        ),
    ]