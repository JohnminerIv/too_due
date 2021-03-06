from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import jsonpickle
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from .models import LoginForm, NewUserForm, GoogleAuthenication, NewHobbyForm, Hobby, ScheduledHobby, NewTaskForm, Task, ScheduledTask, NewToDoForm, ToDo, ScheduledToDo, ScheduleForm


def index(request):
    if request.user.is_authenticated:
        # Try to fetch the authentication token from the session
        if hasattr(request.user, 'googleauthenication'):
            creds = jsonpickle.decode(request.user.googleauthenication.credentials)
        else:
            creds = None
        # If an authentication token does not exist already,
        # create one and store it in the session.
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CRED, settings.GOOGLE_SCOPE)
            creds = flow.run_local_server(port=0)
            auth = GoogleAuthenication(user=request.user, credentials=jsonpickle.encode(creds))
            auth.save()
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        body = {"start": {"date": '2020-3-29'}, "end": {"date": '2020-3-29'}, "summary": 'An Event'}
        event = service.events().get(calendarId='primary', eventId='lcheg2ck3etuuutckkiargsnt0', alwaysIncludeEmail=None, timeZone=None, maxAttendees=None).execute()


        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        return render(request, 'landing_home/index.html', {'user': request.user})
    return render(request, 'landing_home/index.html', {'user': request.user})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['your_username'], password=form.cleaned_data['your_password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('is valid but not a user')
        else:
            return HttpResponse('is not valid')
    else:
        form = LoginForm()
    return render(request, 'landing_home/login_form.html', {'form': form})


def new_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.get(username=form.cleaned_data['your_username'])
            except:
                u = None
            if u is None:
                user = User.objects.create_user(first_name=form.cleaned_data['your_first_name'],
                                                last_name=form.cleaned_data['your_last_name'],
                                                email=form.cleaned_data['your_email'],
                                                username=form.cleaned_data['your_username'],
                                                password=form.cleaned_data['your_password'])
                user.save()
                return HttpResponseRedirect('/user/login/')
            else:
                return HttpResponse('is valid but username already in use')
        else:
            return HttpResponse('is not valid')
    else:
        form = NewUserForm()
    return render(request, 'landing_home/new_user_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'landing_home/index.html')
    # Redirect to a success page.


def hobbies(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewHobbyForm(request.POST)
            if form.is_valid():
                try:
                    hobby = Hobby.objects.get(user=request.user, name=form.cleaned_data['name'])
                except Exception as e:
                    hobby = None
                if hobby is not None:
                    return HttpResponse('This hobby exists already')
                hobby = Hobby.objects.create_hobby(
                                            user=request.user,
                                            name=form.cleaned_data['name'],
                                            enjoyableness=form.cleaned_data['enjoyableness'],
                                            pref_start=form.cleaned_data['pref_start'],
                                            pref_end=form.cleaned_data['pref_end'],
                                            min_time=form.cleaned_data['min_time'])
                hobby.save()
        form = NewHobbyForm()
        hobbies = []
        return render(request, 'landing_home/hobby.html', {'form': form, 'hobbies': hobbies})
    return HttpResponse('Please make an account')


def hobbies_update(request, hobby):
    if request.method == 'POST':
        form = NewHobbyForm(request.POST)
        if form.is_valid():
            hobby = Hobby.objects.get(user=request.user, name=hobby)
            hobby.name = form.cleaned_data['hobby_name']
            hobby.enjoyableness = form.cleaned_data['enjoyableness']
            hobby.pref_start = form.cleaned_data['pref_start']
            hobby.pref_end = form.cleaned_data['pref_end']
            hobby.min_time = form.cleaned_data['min_time']
            hobby.save()
            route = '/hobbies/'+str(hobby.name)+'/'
            return HttpResponseRedirect(route)
    else:
        form = NewHobbyForm()
        hobby = Hobby.objects.get(user=request.user, name=hobby)
        return render(request, 'landing_home/hobby_update.html', {'form': form, 'hobby': hobby})


def hobbies_schedule(request, hobby):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'googleauthenication'):
                creds = jsonpickle.decode(request.user.googleauthenication.credentials)
            else:
                creds = None
            # If an authentication token does not exist already,
            # create one and store it in the session.
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CRED, settings.GOOGLE_SCOPE)
                creds = flow.run_local_server(port=0)
                auth = GoogleAuthenication(user=request.user, credentials=jsonpickle.encode(creds))
                auth.save()
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

            body = {"start": {"date": str(form.cleaned_data['start'])[:10]}, "end": {"date": str(form.cleaned_data['end'])[:10]}, "summary": hobby}
            event = service.events().insert(calendarId='primary', body=body).execute()
            id = event['id']
            hobby = Hobby.objects.get(user=request.user, name=hobby)
            item = ScheduledHobby.objects.create_scheduled_hobby(user=request.user, hobby=hobby, id=id)
            item.save()
            route = '/hobbies/'+str(hobby.name)+'/schedule'
            return HttpResponseRedirect(route)
    else:
        form = ScheduleForm()
        hobby = Hobby.objects.get(user=request.user, name=hobby)
        return render(request, 'landing_home/hobby_update.html', {'form': form, 'hobby': hobby})


def hobbies_delete(request, hobby):
    hobby = Hobby.objects.get(user=request.user, name=hobby)
    hobby.delete()
    return HttpResponseRedirect('/hobbies/')


def tasks(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewTaskForm(request.POST)
            if form.is_valid():
                try:
                    task = Task.objects.get(user=request.user,
                                            name=form.cleaned_data['name'])
                except Exception as e:
                    task = None
                if task is not None:
                    return HttpResponse('This task exists already')
                task = Task.objects.create_task(user=request.user,
                                            name=form.cleaned_data['name'],
                                            enjoyableness=form.cleaned_data['enjoyableness'],
                                            pref_start=form.cleaned_data['pref_start'],
                                            pref_end=form.cleaned_data['pref_end'],
                                            max_time=form.cleaned_data['max_time'],
                                            priority=form.cleaned_data['priority'],
                                            repeated=form.cleaned_data['repeated'])
                task.save()
        form = NewTaskForm()
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'landing_home/task.html', {'form': form, 'tasks': tasks})
    return HttpResponse('Please make an account')


def tasks_update(request, task):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(user=request.user, name=task)
            task.name = form.cleaned_data['name']
            task.enjoyableness = form.cleaned_data['enjoyableness']
            task.pref_start = form.cleaned_data['pref_start']
            task.pref_end = form.cleaned_data['pref_end']
            task.max_time = form.cleaned_data['max_time']
            task.priority = form.cleaned_data['priority']
            task.repeated = form.cleaned_data['repeated']
            task.save()
            route = '/tasks/'+str(task.name)+'/update'
            return HttpResponseRedirect(route)
    else:
        form = NewTaskForm()
        task = Task.objects.get(user=request.user, name=task)
        return render(request, 'landing_home/task_update.html', {'form': form, 'task': task})


def tasks_schedule(request, task):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'googleauthenication'):
                creds = jsonpickle.decode(request.user.googleauthenication.credentials)
            else:
                creds = None
            # If an authentication token does not exist already,
            # create one and store it in the session.
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CRED, settings.GOOGLE_SCOPE)
                creds = flow.run_local_server(port=0)
                auth = GoogleAuthenication(user=request.user, credentials=jsonpickle.encode(creds))
                auth.save()
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

            body = {"start": {"date": str(form.cleaned_data['start'])[:10]}, "end": {"date": str(form.cleaned_data['end'])[:10]}, "summary": task}
            event = service.events().insert(calendarId='primary', body=body).execute()
            id = event['id']
            task = Task.objects.get(user=request.user, name=task)
            item = ScheduledTask.objects.create_scheduled_task(user=request.user, task=task, id=id)
            item.save()
            route = '/tasks/'+str(task.name)+'/schedule'
            return HttpResponseRedirect(route)
    else:
        form = ScheduleForm()
        task = Task.objects.get(user=request.user, name=task)
        return render(request, 'landing_home/task_update.html', {'form': form, 'task': task})


def tasks_delete(request, task):
    task = Task.objects.get(user=request.user, name=task)
    task.delete()
    return HttpResponseRedirect('/tasks/')


def todos(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewToDoForm(request.POST)
            if form.is_valid():
                try:
                    to_do = ToDo.objects.get(user=request.user, name=form.cleaned_data['name'])
                except Exception as e:
                    to_do = None
                if to_do != None:
                    return HttpResponse('This to_do exists already')
                to_do = ToDo.objects.create_to_do(user=request.user,
                                            name=form.cleaned_data['name'],
                                            enjoyableness=form.cleaned_data['enjoyableness'],
                                            pref_start=form.cleaned_data['pref_start'],
                                            pref_end=form.cleaned_data['pref_end'],
                                            max_time=form.cleaned_data['max_time'],
                                            priority=form.cleaned_data['priority'],
                                            total_time=form.cleaned_data['total_time'],
                                            due_date=form.cleaned_data['due_date'])
                to_do.save()
        form = NewToDoForm()
        to_dos = ToDo.objects.filter(user=request.user)
        return render(request, 'landing_home/todo.html', {'form': form, 'to_dos': to_dos})
    return HttpResponse('Please make an account')


def to_dos_update(request, to_do):
    if request.method == 'POST':
        form = NewToDoForm(request.POST)
        if form.is_valid():
            to_do = ToDo.objects.get(user=request.user, name=to_do)
            to_do.name = form.cleaned_data['name']
            to_do.enjoyableness = form.cleaned_data['enjoyableness']
            to_do.pref_start = form.cleaned_data['pref_start']
            to_do.pref_end = form.cleaned_data['pref_end']
            to_do.max_time = form.cleaned_data['max_time']
            to_do.priority = form.cleaned_data['priority']
            to_do.total_time=form.cleaned_data['total_time'],
            to_do.due_date=form.cleaned_data['due_date']
            to_do.save()
            route = '/to_do/'+str(to_do.name)+'/update'
            return HttpResponseRedirect(route)
    else:
        form = NewToDoForm()
        to_do = ToDo.objects.get(user=request.user, name=to_do)
        return render(request, 'landing_home/todo_update.html', {'form': form, 'to_do': to_do})


def to_dos_schedule(request, to_do):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            if hasattr(request.user, 'googleauthenication'):
                creds = jsonpickle.decode(request.user.googleauthenication.credentials)
            else:
                creds = None
            # If an authentication token does not exist already,
            # create one and store it in the session.
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CRED, settings.GOOGLE_SCOPE)
                creds = flow.run_local_server(port=0)
                auth = GoogleAuthenication(user=request.user, credentials=jsonpickle.encode(creds))
                auth.save()
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

            body = {"start": {"date": str(form.cleaned_data['start'])[:10]}, "end": {"date": str(form.cleaned_data['end'])[:10]}, "summary": to_do}
            event = service.events().insert(calendarId='primary', body=body).execute()
            id = event['id']
            to_do = ToDo.objects.get(user=request.user, name=to_do)
            item = ScheduledToDo.objects.create_scheduled_to_do(user=request.user, to_do=to_do, id=id)
            item.save()
            route = '/to_dos/'+str(to_do.name)+'/schedule'
            return HttpResponseRedirect(route)
    else:
        form = ScheduleForm()
        to_do = ToDo.objects.get(user=request.user, name=to_do)
        return render(request, 'landing_home/todo_update.html', {'form': form, 'to_do': to_do})


def to_dos_delete(request, to_do):
    to_do = ToDo.objects.get(user=request.user, name=to_do)
    to_do.delete()
    return HttpResponseRedirect('/to_do/')
