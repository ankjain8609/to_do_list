from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('task_add/', views.task_add, name='task_add'),
    path('completed/',views.tasks_completed_list, name = 'tasks_compeleted_list'),
    path('<int:task_id>/edit/', views.task_edit, name = 'task_edit'),
    path('<int:task_id>/complete/', views.task_complete_home_page, name = 'complete_task_home_page'),
    path('<int:task_id>/delete_home/', views.task_delete_home_page, name = 'delete_task_home'),
    path('<int:task_id>/delete_completed/', views.task_delete_completed_page, name = 'delete_task_completed'),
    path('<int:task_id>/inprogress/', views.task_inprogress, name = 'task_inprogress'), 
    path('<int:task_id>/open_completed/', views.task_open_completed_page, name = 'task_open_completed_page'),
    path('<int:task_id>/log_hours/', views.task_log_hours, name = 'task_log_hours'),
    path('<int:task_id>/log_summary/', views.task_log_summary, name = 'task_log_summary'),
    path('<int:label_id>/label_delete_home_page/', views.label_delete_home_page, name = 'label_delete_home_page'),
    path('<int:label_id>/label_delete_task_add_page/', views.label_delete_task_add_page, name = 'label_delete_task_add_page'),
    #path('label_filter/', views.label_filter, name = 'label_filter'),
]