# Generated by Django 3.1.2 on 2020-10-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('MuscleFeed_main', '0002_auto_20201005_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixed',
            name='phone_number',
            field=models.CharField(default='+7(999)000-00-00', max_length=20, verbose_name='Контактный номер телефона'),
            preserve_default=False,
        ),
    ]
