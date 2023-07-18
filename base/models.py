from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(unique=True, null=False)
    bio = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Project(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    participants = models.ManyToManyField(User, related_name='board_participants', blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=50, default='#default_label')
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class Status(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=10, default='default')
    board = models.ManyToManyField(Board, related_name='status_board')
    step = models.PositiveBigIntegerField(validators=[MaxValueValidator(5)], null = False)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['step']

    def __str__(self):
        return self.name

class Issue(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='issue_participants', blank=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True)
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='assignee')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]