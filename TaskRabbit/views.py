from rest_framework import viewsets, status
from rest_framework.response import Response

from django.db.models import Q

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

from drf_yasg.utils import swagger_auto_schema


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing projects.

    Requires authentication for all operations. Users can create, retrieve, update, and delete projects,
    including assigning members and managing tasks (not implemented in this example).
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @swagger_auto_schema(
        operation_description="List all projects.",
        responses={200: ProjectSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all projects.

        Optionally filter projects by completion status using the 'completed' query parameter (true/false).
        """
        completed = request.query_params.get('completed', None)
        queryset = self.get_queryset()
        if completed is not None:
            # Filter based on completed tasks
            completed_tasks_q = Q(tasks__complete=True)
            total_tasks_q = Q(tasks__id__in=self.tasks.filter(project=self.pk).values_list('id', flat=True))
            if completed == 'true':
                queryset = queryset.filter(completed_tasks_q & total_tasks_q)
            else:
                queryset = queryset.exclude(completed_tasks_q & total_tasks_q)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get a specific project by ID.",
        responses={200: ProjectSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific project by its ID.
        """
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new project.",
        request_body=ProjectSerializer,
        responses={201: ProjectSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new project.

        The request body should include all required project fields as specified in the ProjectSerializer class.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_header(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description="Update a project with the provided ID.",
        request_body=ProjectSerializer,
        responses={200: ProjectSerializer}
    )
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update a project with the provided ID.

        The request body should include the updated project data as specified in the ProjectSerializer class.
        """
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @swagger_auto_schema(
      operation_description="Delete a project with the provided ID.",
      responses={204: "Project deleted successfully."}
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing tasks.

    Users can create, retrieve, update, and delete tasks associated
    with a specific project.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="""
        Retrieve a list of all tasks.

        Optionally filter tasks based on various criteria using request query parameters:
            * project: Filter tasks associated with a specific project ID.
            * completed: Filter tasks based on their completion status (true/false).
        """,
        responses={200: TaskSerializer(many=True)},
        query_serializer=TaskSerializer  # Allow filtering by task fields in request
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all tasks.

        Optionally filter tasks based on various criteria using request query parameters:
            * project: Filter tasks associated with a specific project ID.
            * completed: Filter tasks based on their completion status (true/false).
        """
        queryset = self.get_queryset()
        project_id = request.query_params.get('project', None)
        completed = request.query_params.get('completed', None)

        if project_id:
            queryset = queryset.filter(project=project_id)
        if completed is not None:
            queryset = queryset.filter(complete=completed)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get a specific task by ID.",
        responses={200: TaskSerializer}
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific task by its ID.
        """
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new task within a specific project.",
        request_body=TaskSerializer,
        responses={201: TaskSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new task associated with a specific project.

        The request body should include all required task fields and the 'project' field specifying the project ID.
        """
        project_id = request.data.get('project')
        if not project_id:
            return Response({'error': 'Missing project ID in request data.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project with provided ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)  # Set the project relationship explicitly
        headers = self.get_success_header(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description="Update a task with the provided ID.",
        request_body=TaskSerializer,
        responses={200: TaskSerializer}
    )
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update a task with the provided ID.

        The request body should include the updated task data as specified in the TaskSerializer class.
        """
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # No need to set project as it's already linked
        return Response(serializer.data)
    
    @swagger_auto_schema(
      operation_description="Delete a task with the provided ID.",
      responses={204: "Task deleted successfully."}
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
