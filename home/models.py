from django.db import models
from django.contrib.auth.models import User

class UserProfileREADME(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="""
    # Nexify - Management & Progress Tracking Platform

    Welcome to **Nexify**! This platform is designed to streamline the management, tracking, and accountability of club activities, goals, and progress. Whether you're leading a team or a member of a club, Nexify makes it easy to stay on top of your responsibilities and engage in meaningful progress tracking.

    ## Features

    - **Club Management**: Easily manage your clubs, societies, or teams. Assign roles and track club activities with ease.
    - **Task & Goal Tracking**: Create, assign, and track tasks and goals for your club members, ensuring accountability.
    - **Progress Monitoring**: Visualize progress over time with dynamic charts, logs, and reports.
    - **User Roles**: Different roles like Admin and Member, with customizable access to manage club events and activities.
    - **Event Management**: Organize events, track participation, and send reminders to members.
    - **Notifications**: Get timely notifications about upcoming tasks, deadlines, and updates.
    - **Communication Tools**: Streamlined communication channels for better coordination between club members.

    ## Getting Started

    ### Prerequisites

    Before getting started with Nexify, ensure you have the following:
    - A modern web browser (e.g., Chrome, Firefox)
    - A registered account on **Nexify** (Sign up on the platform)
""")  # Markdown content
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s README"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="John Doe")
    bio = models.CharField(max_length=50,default="Meow meow")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,default='../static/assets/img/profile_default/logo.jpeg')
    background_picture = models.ImageField(upload_to='profile_background/', blank=True,default='../static/assets/img/profile_default/background.png')

    address=models.CharField(max_length=100,default="John Doe Business space")
    insta=models.CharField(max_length=100,default='https://www.instagram.com')
    github=models.CharField(max_length=100,default="https://github.com")
    linkedin=models.CharField(max_length=100,default="https://www.linkedin.com")
    twitter=models.CharField(max_length=100,default="https://www.twitter.com")
    website=models.CharField(max_length=100,default="https://example.com")

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"


    