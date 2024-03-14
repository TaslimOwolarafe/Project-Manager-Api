from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
  members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())  # Use User model from Django auth

  class Meta:
    model = Project
    fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'