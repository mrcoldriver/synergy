# Generated by Django 2.2.10 on 2020-07-04 11:11

import backend.occupations_list.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('occupations_list', '0003_auto_20200704_1439'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AlterField(
            model_name='occupation',
            name='hire_date',
            field=models.DateField(default=backend.occupations_list.models.get_due_date, verbose_name='Дата приема'),
        ),
    ]
