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
    hobby_name = forms.CharField(label='Hobby', max_length=100)


class HobbyManager(models.Manager):
    def create_hobby(self, name, user):
        hobby = self.create(name=name, user=user)
        return hobby


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    task_name = forms.CharField(label='Task', max_length=100)


class TaskManager(models.Manager):
    def create_task(self, name, user):
        task = self.create(name=name, user=user)
        return task


class Task(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = TaskManager()


class ScheduledTaskManager(models.Manager):
    def create_scheduled_task(self, user, task, id):
        task = self.create(user=user, task=task, calendar_id=id)
        return task


class ScheduledTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=100)


class NewToDoForm(forms.Form):
    to_do_name = forms.CharField(label='To_do', max_length=100)


class ToDoManager(models.Manager):
    def create_to_do(self, name, user):
        to_do = self.create(name=name, user=user)
        return to_do


class ToDo(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = ToDoManager()


class ScheduledToDoManager(models.Manager):
    def create_scheduled_to_do(self, user, to_do, id):
        to_do = self.create(user=user, to_do=to_do, calendar_id=id)
        return to_do


class ScheduledToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_do = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=100)


class ScheduleForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()
