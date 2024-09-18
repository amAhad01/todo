from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='todo_list'),
    path('todo/<int:pk>/', views.detail, name='todo_detail'),
    path('add/', views.addlist, name='add_todo_list'),
    path('todo/<int:pk>/delete/', views.deletelist, name='delete_todo_list'),
    path('todo/<int:pk>/add_task/', views.add_task, name='add_task'),
    path('todo/<int:pk>/task/<int:task_pk>/edit/', views.edit_task, name='edit_task'),
    path('todo/<int:pk>/task/<int:task_pk>/delete/', views.delete_task, name='delete_task'),
    path('signup/', views.signUp, name='sign_up'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('changepass/', views.changePass, name='changepass')
]
