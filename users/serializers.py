from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class FeedbackSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSettings
        fields = "__all__"


class CompanyEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEvaluation
        fields = '__all__'


class EmployeeEvaluationSeializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEvaluation
        fields = '__all__'
