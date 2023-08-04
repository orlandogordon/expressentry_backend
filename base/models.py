from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
# Create your models here.

class User(AbstractUser): 
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    hackathon_participant = models.BooleanField(default=True, null=True)

    avatar = ResizedImageField(size=[250,250], crop=['middle', 'center'], upload_to="images/", default='images/default-avatar.png')

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    twitter = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    github = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)

class Event(models.Model):
    # Event Type Choices
    CHOICES = (
        ('hackathon', 'Hackathon'),
        ('seminar', 'Seminar'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    event_type = models.CharField(max_length=100, choices=CHOICES, default='hackathon')
    cover_photo = ResizedImageField(size=[2400,1600], crop=['middle', 'center'], upload_to="images/", default='images/default-hackathon.png')
    participants = models.ManyToManyField(User, blank=True, related_name='events') 
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.name

    
class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submissions')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    demo = models.URLField(max_length=500, null=True)
    details = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    
    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)
