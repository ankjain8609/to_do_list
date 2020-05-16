from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.add_task, name='add_task'),
    path('completed/',views.list_completed_tasks, name = 'list_completed_tasks'),
    path('<int:task_id>/edit/', views.edit_task, name = 'edit_task'),
    path('<int:task_id>/complete/', views.complete_task_home_page, name = 'complete_task_home_page'),
    path('<int:task_id>/delete_home/', views.delete_task_home_page, name = 'delete_task_home'),
    path('<int:task_id>/delete_completed/', views.delete_task_completed_page, name = 'delete_task_completed'),
    path('<int:task_id>/inprogress/', views.inprogress_task, name = 'inprogress_task'), 
    path('<int:task_id>/open_completed/', views.open_task_completed_page, name = 'open_task_completed_page')
]