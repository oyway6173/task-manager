from django.contrib import admin

from .models import User, Board, Status, Issue, Project, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(Board)
admin.site.register(Status)
admin.site.register(Issue)
admin.site.register(Project)
admin.site.register(Comments)
