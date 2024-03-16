from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

from datetime import datetime

class ProjectSerializer(serializers.ModelSerializer):
  members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

  class Meta:
    model = Project
    fields = '__all__'
    
  def validate(self, data):
        # Check if due_date is greater than the current date
        if 'due_date' in data:
            due_date = data['due_date']
            if due_date <= datetime.now().date():
                raise serializers.ValidationError("Due date must be greater than the current date.")

        # Check if title is not null
        if 'title' in data:
            title = data['title']
            if not title:
                raise serializers.ValidationError("Title cannot be empty.")

        return data

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'