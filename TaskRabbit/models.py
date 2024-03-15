from django.db import models

class Project(models.Model):
  title = models.CharField(max_length=255)
  display_photo = models.ImageField(upload_to='project_photos/', blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  due_date = models.DateField(blank=True, null=True)
  members = models.ManyToManyField('auth.User', related_name='projects', blank=True)
  
  def is_completed(self):
    """
    Checks if all tasks associated with the project are completed.

    This method assumes a Task model with a 'complete' boolean field and a foreign key relationship to the Project model.
    """
    return self.tasks.filter(complete=True).count() == self.tasks.count()

  def __str__(self):
    return self.title

class Task(models.Model):
  title = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
  complete = models.BooleanField(default=False)

  def __str__(self):
    return self.title