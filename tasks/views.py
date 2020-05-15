from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Tasks
from .forms import TaskCreationForm, TaskUpdationForm
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    tasks_not_done = Tasks.objects.exclude(task_status ='Done')
    context = { 'tasks_not_done': tasks_not_done}
    return render(request, 'tasks/index.html', context)

def add_task(request):
    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_status = 'Open'
            task.task_create_time = timezone.now()
            task.task_last_updated_time = timezone.now()
            task.save()
            
            context = tasks_home_page_context()
            return render(request, 'tasks/index.html', context)
    else:
        form = TaskCreationForm()
    
    return render(request, 'tasks/edit_task.html', {'form': form})

def edit_task(request, task_id):
    task = Tasks.objects.get(id = task_id)
    if request.method == "POST": 
        form = TaskUpdationForm(request.POST, instance = task)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_last_updated_time = timezone.now()
            task.save()
            
            context = tasks_home_page_context()
            return render(request, 'tasks/index.html', context)
    else: 
        form = TaskUpdationForm(instance = task)
    
    return render(request, 'tasks/edit_task.html', {'form': form})    

def complete_task(request, task_id):
    task = Tasks.objects.get(id = task_id)
    #form = TaskUpdationForm(request.POST, instance = task)
    task.task_status = 'Done'
    task.task_last_updated_time = timezone.now()
    task.task_completed_time = timezone.now()
    task.save()
            
    context = tasks_home_page_context()
    return render(request, 'tasks/index.html', context)

def list_completed_tasks(request):
    tasks_done = Tasks.objects.filter(task_status='Done')
    context = {'tasks_done': tasks_done}
    return render(request, 'tasks/completed_tasks.html', context)

def tasks_home_page_context():
    tasks_not_done = Tasks.objects.exclude(task_status ='Done')
    context = { 'tasks_not_done': tasks_not_done}
    return context

    