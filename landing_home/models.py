from django.db import models
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    your_username = forms.CharField(label='Your Username', max_length=100)
    your_password = forms.CharField(label='Your password', max_length=100)


class NewUserForm(forms.Form):
    your_first_name = forms.CharField(label='Your First Name', max_length=100)
    your_last_name = forms.CharField(label='Your Last Name', max_length=100)
    your_email = forms.CharField(label='Your Email', max_length=100)
    your_username = forms.CharField(label='Your Username', max_length=100)
    your_password = forms.CharField(label='Your Password', max_length=100)


class GoogleAuthenication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    credentials = models.CharField(max_length=10000)


class NewHobbyForm(forms.Form):
    name = forms.CharField(label='Hobby', max_length=100)
    enjoyableness = forms.ChoiceField([str(i) for i in range(6)])
    pref_start = forms.CharField(max_length=5)
    pref_end = forms.CharField(max_length=5)
    min_time = forms.CharField(max_length=5)


class HobbyManager(models.Manager):
    def create_hobby(self, name, user, enjoyableness, pref_start, pref_end, min_time):
        hobby = self.create(name=name,
                            user=user,
                            enjoyableness=enjoyableness,
                            pref_start=pref_start,
                            pref_end=pref_end,
                            min_time=min_time)
        return hobby


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pref_start = models.CharField(max_length=5)
    pref_end = models.CharField(max_length=5)
    min_time = models.CharField(max_length=5)
    enjoyableness = models.CharField(max_length=1)
    objects = HobbyManager()


class ScheduledHobbyManager(models.Manager):
    def create_scheduled_hobby(self, user, hobby, id):
        hobby = self.create(user=user, hobby=hobby, calendar_id=id)
        return hobby


class ScheduledHobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=100)
    objects = ScheduledHobbyManager()


class NewTaskForm(forms.Form):
    name = forms.CharField(label='Task', max_length=100)
    priority = forms.ChoiceField([str(i) for i in range(1, 11)])
    enjoyableness = forms.ChoiceField([str(i) for i in range(-5, 6)])
    pref_start = forms.CharField(max_length=5)
    pref_end = forms.CharField(max_length=5)
    max_time = forms.CharField(max_length=5)
    repeated = forms.ChoiceField([str(i) for i in range(1, 30)])


class TaskManager(models.Manager):
    def create_task(self, name, user, enjoyableness, pref_start, pref_end, max_time, repeated=repeated):
        task = self.create(name=name,
                            user=user,
                            enjoyableness=enjoyableness,
                            pref_start=pref_start,
                            pref_end=pref_end,
                            max_time=max_time,
                            repeated=repeated,
                            priority=priority)
        return task


class Task(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pref_start = models.CharField(max_length=5)
    pref_end = models.CharField(max_length=5)
    min_time = models.CharField(max_length=5)
    enjoyableness = models.CharField(max_length=1)
    repeated = models.CharField(max_length=2)
    priority = models.CharField(max_length=2)
    objects = TaskManager()


class ScheduledTaskManager(models.Manager):
    def create_scheduled_task(self, user, task, id):
        task = self.create(user=user, task=task, calendar_id=id)
        return task


class ScheduledTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=100)
    objects = ScheduledTaskManager()


class NewToDoForm(forms.Form):
    name = forms.CharField(label='To_do', max_length=100)
    priority = forms.ChoiceField([str(i) for i in range(1, 11)])
    enjoyableness = forms.ChoiceField([str(i) for i in range(-5, 6)])
    pref_start = forms.CharField(max_length=5)
    pref_end = forms.CharField(max_length=5)
    max_time = forms.CharField(max_length=5)
    due_date = forms.DateTimeField()
    total_time = max_time = forms.CharField(max_length=10)


class ToDoManager(models.Manager):
    def create_to_do(self, name, user, enjoyableness, pref_start, pref_end, max_time, priority, due_date, total_time):
        to_do = self.create(name=name,
                            user=user,
                            enjoyableness=enjoyableness,
                            pref_start=pref_start,
                            pref_end=pref_end,
                            max_time=max_time,
                            priority=priority,
                            due_date=due_date,
                            total_time=total_time)
        return to_do


class ToDo(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pref_start = models.CharField(max_length=5)
    pref_end = models.CharField(max_length=5)
    min_time = models.CharField(max_length=5)
    enjoyableness = models.CharField(max_length=1)
    priority = models.CharField(max_length=2)
    total_time = models.CharField(max_length=10)
    due_date = models.DateTimeField()
    objects = ToDoManager()


class ScheduledToDoManager(models.Manager):
    def create_scheduled_to_do(self, user, to_do, id):
        to_do = self.create(user=user, to_do=to_do, calendar_id=id)
        return to_do


class ScheduledToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_do = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=100)
    objects = ScheduledToDoManager()


class ScheduleForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()
