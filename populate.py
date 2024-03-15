import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "benmore.settings")

import django
django.setup()


from TaskRabbit.models import Project, Task

from faker import Faker
from django.contrib.auth.models import User
from PIL import Image
import os

from pathlib import Path
from random import randint

# Create a Faker instance
fake = Faker()


# Function to generate random project data with a saved image
def generate_project_data():
    title = fake.company()

    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)

    # Create a new image with random color
    image = Image.new("RGB", (200, 200), color=(red, green, blue))

    # Create a unique filename using project title
    filename = f"project_images/{title}.jpg"


    os.makedirs("project_images", exist_ok=True) 

    # Save the image to the specified path
    image.save(filename)

    due_date = fake.future_date(end_date='+30d')
    return {
        'title': title,
        'display_photo': filename,  # Store the image filename
        'due_date': due_date,
    }


# Function to generate random task data
def generate_task_data(project):
    title = fake.sentence()
    return {
        'title': title,
        'project': project,
    }


# Create 10 projects with 20 tasks each
for _ in range(10):
    project_data = generate_project_data()
    project = Project.objects.create(**project_data)  # Create project object first
    path = Path(project_data['display_photo'])
    with path.open(mode='rb') as f:
        project.display_photo.save(content=f, name=path.name)
    
    members = [User.objects.get_or_create(username=fake.name().lower())[0] for _ in range(2)]  # Create or get 2 random users
    for user in members:
        project.members.add(user)
    
    for _ in range(20):
        task_data = generate_task_data(project)
        Task.objects.create(**task_data)  # Create task object and associate with project

    print(f"Created project {project.title} with 20 tasks")


print("Created 10 projects with 20 tasks each!")

