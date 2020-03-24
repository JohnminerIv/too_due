from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/new/', views.new_user, name='new_user'),
    path('user/logout/', views.logout_view, name='user_logout'),
    path('hobbies/', views.hobbies, name='hobbies'),
    path('hobbies/<str:hobby>/update/', views.hobbies_update, name='hobbies_update'),
    path('hobbies/<str:hobby>/delete/', views.hobbies_delete, name='hobbies_delete'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<str:task>/update/', views.tasks_update, name='tasks_update'),
    path('tasks/<str:task>/delete/', views.tasks_delete, name='tasks_delete'),
    path('to_dos/', views.todos, name='to_dos'),
    path('to_dos/<str:to_do>/update/', views.to_dos_update, name='to_dos_update'),
    path('to_dos/<str:to_do>/delete/', views.to_dos_delete, name='to_dos_delete'),
    path('hobbies/<str:hobby>/schedule/', views.hobbies_schedule, name='schedule')
]
