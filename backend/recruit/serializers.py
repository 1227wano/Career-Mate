from rest_framework import serializers
from .models import Job
from companies.models import Company
from companies.serializers import CompanySerializer


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
