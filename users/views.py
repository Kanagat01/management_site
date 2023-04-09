import datetime
import os
from .serializers import *
from .models import *
from .forms import *
from matplotlib import pyplot as plt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics
import matplotlib
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CompanyAPIList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class FeedbackSettingsAPIList(generics.ListAPIView):
    queryset = FeedbackSettings.objects.all()
    serializer_class = FeedbackSettingsSerializer


class EmployeeAPIList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CompanyEvaluationAPI(generics.ListCreateAPIView):
    queryset = CompanyEvaluation.objects.all()
    serializer_class = CompanyEvaluationSerializer


class EmployeeEvaluationAPI(generics.ListCreateAPIView):
    queryset = EmployeeEvaluation.objects.all()
    serializer_class = EmployeeEvaluationSeializer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = CompanyUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.company)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Ваши данные успешно обновлены.')
            return redirect('home')

    else:
        company = request.user.company
        employees_count = Employee.objects.filter(company=company).count()
        company.num_of_employees = employees_count
        company.save()
        u_form = UserUpdateForm(instance=request.user)
        p_form = CompanyUpdateForm(instance=company)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/home.html', context)


@login_required
def results(request):
    company = Company.objects.get(company_name=request.user.company)
    employees = Employee.objects.filter(company=company)
    compEval = CompanyEvaluation.objects.filter(company=company)
    empEval = EmployeeEvaluation.objects.filter(company=company)

    for employee in employees:
        data = compEval.filter(employee=employee)
        x = [datetime.datetime.strptime(
            str(d.time_create), '%Y-%m-%d') for d in data]
        y = [d.evaluation for d in data]
        plt.plot(x, y)
        plt.xlabel('Дата оценки')
        plt.ylabel('Оценка')
        plt.title(
            f'Оценки сотрудника {employee.fullname} о компании')
        plt.xticks(x, rotation=90)  # type: ignore
        plt.savefig(os.path.join(BASE_DIR,
                    f'users/static/users/images/{employee.pk}_result.png'))
        plt.clf()

        for colleague in employees:
            if colleague != employee:
                data = empEval.filter(evaluator=colleague)
                x = [datetime.datetime.strptime(
                    str(d.time_create), '%Y-%m-%d') for d in data]
                y = [d.evaluation for d in data]
                plt.plot(x, y)
                plt.xlabel('Дата оценки')
                plt.ylabel('Оценка')
                plt.title(
                    f'Оценки коллеги {colleague.fullname} о сотруднике {employee.fullname}')
                plt.xticks(x, rotation=90)  # type: ignore
                plt.savefig(
                    os.path.join(BASE_DIR, f'users/static/users/images/{colleague.pk}_{employee.pk}_result.png'))
                plt.clf()

    return render(request, 'users/results.html', {'employees': employees})


@login_required
def employees(request):
    company = Company.objects.get(company_name=request.user.company)
    employees = Employee.objects.filter(company=company)

    if request.method == 'POST':
        employee1_fullname = request.POST.get('employee1_fullname')
        if employee1_fullname is not None:
            FeedbackSettings.objects.filter(company=company.pk).delete()
            for employee in employees:
                if request.POST.get(f"{employee.pk}_evaluator") == "on":
                    surveys_for_month = request.POST.get(
                        f"{employee.pk}_surveys_for_month")

                    FeedbackSettings.objects.create(
                        employee1_fullname=employee1_fullname,
                        employee2_tg_id=employee.telegram_id,
                        surveys_for_month=surveys_for_month,
                        company=company
                    )

        feedback_settings = FeedbackSettings.objects.filter(company=company.pk)
        tg_ids = [int(id) for id in feedback_settings.values_list(
            'employee2_tg_id', flat=True)]

        context = {
            'employees': employees,
            'first_setting': feedback_settings.first(),
            'tg_ids': tg_ids,
            'surveys_for_month': {id: FeedbackSettings.objects.get(employee2_tg_id=id).surveys_for_month for id in tg_ids}
        }
        return render(request, 'users/employees.html', context)
