from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Tasks, Labels
from .forms import TaskCreationForm, TaskUpdationForm, LabelCreationForm
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    if request.method == "POST":
        form = LabelCreationForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.label_create_time = timezone.now()
            label.save()
                
            form = LabelCreationForm()
            tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
            tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
            tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')
            tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
            context = { 'tasks_not_done': tasks_not_done, 'tasks_in_progress': tasks_in_progress, 'form': form}
            return render(request, 'tasks/index.html', context)
    else:
        form = LabelCreationForm()

    tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
    tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
    tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')

    tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
    context = { 'tasks_not_done': tasks_not_done, 'tasks_in_progress': tasks_in_progress, 'form': form}
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
    return task

def complete_task_home_page(request, task_id):
    task = complete_task(request, task_id)
    context = tasks_home_page_context()
    return render(request, 'tasks/index.html', context)

def inprogress_task(request, task_id):
    task = Tasks.objects.get(id = task_id)
    #form = TaskUpdationForm(request.POST, instance = task)
    task.task_status = 'In Progress'
    task.task_last_updated_time = timezone.now()
    task.save()
    context = tasks_home_page_context()
    return render(request, 'tasks/index.html', context)

def delete_task(request, task_id):
    task = Tasks.objects.get(id = task_id)
    #form = TaskUpdationForm(request.POST, instance = task)
    task.task_status = 'Deleted'
    task.task_last_updated_time = timezone.now()
    task.save()
    return task    

def delete_task_home_page(request, task_id):
    task = delete_task(request, task_id)
    context = tasks_home_page_context()
    return render(request, 'tasks/index.html', context)

def delete_task_completed_page(request, task_id):
    task = delete_task(request, task_id)
    tasks_done = Tasks.objects.filter(task_status='Done')
    context = {'tasks_done': tasks_done}
    return render(request, 'tasks/completed_tasks.html', context)

def list_completed_tasks(request):
    tasks_done = Tasks.objects.filter(task_status='Done')
    context = {'tasks_done': tasks_done}
    return render(request, 'tasks/completed_tasks.html', context)

def open_task_completed_page(request, task_id):
    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Open'
    task.task_last_updated_time = timezone.now()
    task.task_completed_time = None
    task.save()

    context = tasks_home_page_context()
    return render(request, 'tasks/index.html', context)
"""    
def list_completed_tasks(request):
    context = tasks_completed_page_context(request)
    return render(request, 'tasks/completed_tasks.html', context)
"""
def tasks_home_page_context():
    tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
    tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
    tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')

    tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
    context = { 'tasks_not_done': tasks_not_done, 'tasks_in_progress': tasks_in_progress}
    return context

#def add_label(request):

   