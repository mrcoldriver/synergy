
import backend.occupations_list.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [

        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Имя')),
                ('company_name', models.CharField(max_length=100, verbose_name='Компания')),
                ('position_name', models.CharField(max_length=100, verbose_name='Должность')),
                ('hire_date', models.DateField(verbose_name='Дата приема')),
                ('fire_date', models.DateField(null=True, verbose_name='Дата увольнения')),
                ('salary', models.IntegerField(verbose_name='Ставка, руб.')),
                ('fraction', models.IntegerField(verbose_name='Ставка, %')),
                ('base', models.IntegerField(verbose_name='База, руб.')),
                ('advance', models.IntegerField(verbose_name='Аванс')),
                ('by_hours', models.BooleanField(verbose_name='Почасовая оплата')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('-hire_date',),
            },
        ),
    ]
