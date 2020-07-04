from datetime import timedelta

from django.db import models
from django.utils import timezone


def get_due_date():
    return timezone.now() + timedelta(days=1)


class Occupation(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Имя")
    company_name = models.CharField(max_length=100, verbose_name="Компания")
    position_name = models.CharField(max_length=100, verbose_name="Должность")
    hire_date = models.DateField(default=get_due_date, verbose_name="Дата приема")
    fire_date = models.DateField(null=True, verbose_name="Дата увольнения")
    salary = models.IntegerField(verbose_name="Ставка, руб.")
    fraction = models.IntegerField(verbose_name="Ставка, %")
    base = models.IntegerField(verbose_name="База, руб.")
    advance = models.IntegerField(verbose_name="Аванс")
    by_hours = models.BooleanField(verbose_name="Почасовая оплата")

    class Meta:
        ordering = ('-hire_date',)
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name
