# Generated by Django 3.1.2 on 2021-05-26 19:06 

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MuscleFeed_main', '0045_auto_20210526_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MuscleFeed_main.menutype', verbose_name='Тип меню'),
        ),
    ]
