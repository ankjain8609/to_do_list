from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.add_task, name='add_task'),
    path('completed/',views.list_completed_tasks, name = 'list_completed_tasks'),
    path('<int:task_id>/edit/', views.edit_task, name = 'edit_task'),
    path('<int:task_id>/complete/', views.complete_task, name = 'complete_task')
]