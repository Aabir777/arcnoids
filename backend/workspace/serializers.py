from rest_framework import serializers
from .models import Client, Project, Task, Enquiry
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields="__all__"
        read_only_fields=("id","created_by","created_at","updated_at")
class ProjectSerializer(serializers.ModelSerializer):
    client_name=serializers.CharField(source="client.name",read_only=True)
    class Meta:
        model=Project
        fields=("id","name","client","client_name","description","status","due_date","members","created_by","created_at","updated_at")
        read_only_fields=("id","created_by","created_at","updated_at")
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields="__all__"
        read_only_fields=("id","created_by","created_at","updated_at")
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model=Enquiry
        fields="__all__"
        read_only_fields=("id","created_by","created_at","updated_at")
