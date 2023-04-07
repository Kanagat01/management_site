from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db import transaction
from .models import Company, Employee, FeedbackSettings


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Ваш email')
    company_name = forms.CharField(
        label='Название компании', max_length=16,
        validators=[
            RegexValidator(
                r'^[a-zA-Z]+$',
                'Название компании должно состоять только из латинских букв'
            )
        ])

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'company_name', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        if self.cleaned_data.get('company_name'):
            Company.objects.create(
                user=user, company_name=self.cleaned_data.get('company_name'))
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CompanyUpdateForm(forms.ModelForm):
    company_name = forms.CharField(
        label='Название компании', max_length=16,
        validators=[RegexValidator(r'^[a-zA-Z]+$',
                                   message='Название компании должно содержать только латинские буквы.')])

    class Meta:
        model = Company
        fields = ['company_name', 'num_of_employees', 'code']
        labels = {
            'code': 'Код компании. По этому коду сотрудники смогут добавляться к компании через телеграм бот.',
            'num_of_employees': 'Количество сотрудников',
        }
        widgets = {
            'code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'num_of_employees': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
