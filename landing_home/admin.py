from django.contrib import admin
from .models import Hobby, Task, ToDo, ScheduledTask, ScheduledToDo, ScheduledHobby


admin.site.register(Hobby)
admin.site.register(ScheduledHobby)
admin.site.register(Task)
admin.site.register(ScheduledTask)
admin.site.register(ToDo)
admin.site.register(ScheduledToDo)
