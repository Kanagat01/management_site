from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('employees/', employees, name='employees'),
    path('results/', results, name='results'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('api/companies/', CompanyAPIList.as_view()),
    path('api/feedback_settings/', FeedbackSettingsAPIList.as_view()),
    path('api/employees/', EmployeeAPIList.as_view()),
    path('api/employees/<int:pk>/', EmployeeAPIUpdate.as_view()),
    path('api/company_evaluation/', CompanyEvaluationAPI.as_view()),
    path('api/employee_evaluation/', EmployeeEvaluationAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
