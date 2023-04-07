from django.db import models
from django.contrib.auth.models import User
import random


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=16, unique=True)
    code = models.IntegerField(unique=True)
    num_of_employees = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = random.randint(100000, 999999)
        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Employee(models.Model):
    fullname = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, to_field='code')
    telegram_id = models.IntegerField(unique=True)
    telegram_nickname = models.CharField(max_length=50)
    surveys_for_week = models.IntegerField(default=5)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.fullname


class FeedbackSettings(models.Model):
    employee1_fullname = models.CharField(max_length=255)
    employee2_tg_id = models.CharField(max_length=255)
    surveys_for_month = models.IntegerField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE)


class CompanyEvaluation(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, to_field='telegram_id')
    evaluation = models.IntegerField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, to_field='code')
    time_create = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оценка Компании'
        verbose_name_plural = 'Оценки Компаний'


class EmployeeEvaluation(models.Model):
    evaluator = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='evaluator', to_field='telegram_id')
    evaluation_employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='evaluation_employee', to_field='telegram_id')
    evaluation = models.IntegerField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, to_field='code')
    time_create = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оценка Сотрудника'
        verbose_name_plural = 'Оценка Сотрудников'
