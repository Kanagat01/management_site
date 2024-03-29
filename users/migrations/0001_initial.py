# Generated by Django 4.1.7 on 2023-04-05 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=16, unique=True)),
                ('code', models.IntegerField(unique=True)),
                ('num_of_employees', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('telegram_id', models.IntegerField(unique=True)),
                ('telegram_nickname', models.CharField(max_length=50)),
                ('surveys_for_week', models.IntegerField(default=5)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', to_field='code')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='FeedbackSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee1_fullname', models.CharField(max_length=255)),
                ('employee2_tg_id', models.CharField(max_length=255)),
                ('surveys_for_month', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.IntegerField()),
                ('time_create', models.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', to_field='code')),
                ('evaluation_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_employee', to='users.employee', to_field='telegram_id')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluator', to='users.employee', to_field='telegram_id')),
            ],
            options={
                'verbose_name': 'Оценка Сотрудника',
                'verbose_name_plural': 'Оценка Сотрудников',
            },
        ),
        migrations.CreateModel(
            name='CompanyEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.IntegerField()),
                ('time_create', models.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company', to_field='code')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employee', to_field='telegram_id')),
            ],
            options={
                'verbose_name': 'Оценка Компании',
                'verbose_name_plural': 'Оценки Компаний',
            },
        ),
    ]
