from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse


from django.urls import reverse
from django.views import generic, View
from datetime import datetime
from .models import Game
"""
class IndexView(generic.ListView):
    template_name = 'landing_page/index.html'
    model = Game

    def get(self, request):
        games = self.get_queryset().all()
        return render(request, self.template_name, {"games": games})


class ShowTimeView(View):

    def get(self, request):
        now = datetime.now()
        html = f"<html>It is now {now}. </html>"
        return HttpResponse(html)
"""
def index(request):
    return HttpResponse("Hello, world. You're at the landing_home index.")


def login_form(request):
    return HttpResponse("Hello, world. You're at the login_form index.")


def login_veiw(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def new_user(requst):
    pass


def create_user(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    pass


def logout_view(request):
    logout(request)
    # Redirect to a success page.
