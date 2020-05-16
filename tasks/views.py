from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Tasks, Labels
from .forms import TaskCreationForm, TaskUpdationForm, LabelCreationForm
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect

#View, Home Page
def index(request):
    
    if request.method == "POST":
    #Label Creation Form    
        form = LabelCreationForm(request.POST)
        
        if form.is_valid():
        
            label = form.save(commit=False)
            label.label_create_time = timezone.now()
            label.save()
                
            form = LabelCreationForm()
            #Set of parameters that need to be passed in the home page template.
            context = home_page_context()  
            context['form'] = form
            
            return render(request, 'tasks/index.html', context)
    else:

        form = LabelCreationForm()
        context = home_page_context()
        context['form'] = form
        
        return render(request, 'tasks/index.html', context)

#View, Add Task
def task_add(request):

    if request.method == "POST":
    #Task Creation Form       
        form = TaskCreationForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.task_status = 'Open'
            task.task_create_time = timezone.now()
            task.task_last_updated_time = timezone.now()
            task.save()
            
            #Context to be passed to the home page
            form = LabelCreationForm()
            context = home_page_context()
            context['form'] = form
            return render(request, 'tasks/index.html', context)
    else:
        form = TaskCreationForm()
    
    return render(request, 'tasks/edit_task.html', {'form': form})

#View, Edit Task
def task_edit(request, task_id):
    task = Tasks.objects.get(id = task_id)
    
    if request.method == "POST": 
    #Task Updation Form
        form = TaskUpdationForm(request.POST, instance = task)

        if form.is_valid():
            task = form.save(commit=False)
            task.task_last_updated_time = timezone.now()
            task.save()
            
            #Context to be passed to the home page
            form = LabelCreationForm()
            context = home_page_context()
            context['form'] = form            
            return render(request, 'tasks/index.html', context)
    else: 
        form = TaskUpdationForm(instance = task)
    
    return render(request, 'tasks/task_edit.html', {'form': form})    

#Controller, Mark Task Status as Complete 
def task_complete(request, task_id):

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Done'
    task.task_last_updated_time = timezone.now()
    task.task_completed_time = timezone.now()
    task.save()

    return task

#View, Change the home page view when a task is marked as complete.
def task_complete_home_page(request, task_id):

    task = task_complete(request, task_id)
    
    #Context to be passed to the home page
    form = LabelCreationForm()
    context = home_page_context()
    context['form'] = form            

    return render(request, 'tasks/index.html', context)

#View, Change the home page view when a task is marked as in progress.
def task_inprogress(request, task_id):
    
    task = Tasks.objects.get(id = task_id)
    task.task_status = 'In Progress'
    task.task_last_updated_time = timezone.now()
    task.save()

    #Context to be passed to the home page
    form = LabelCreationForm()
    context = home_page_context()
    context['form'] = form            

    return render(request, 'tasks/index.html', context)
    
#Controller, Mark Task Status as Complete 
def task_delete(request, task_id):

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Deleted'
    task.task_last_updated_time = timezone.now()
    task.save()

    return task    

#View, Change the home page view when a task is deleted. 
def task_delete_home_page(request, task_id):

    task = task_delete(request, task_id)
    
    #Context to be passed to the home page
    form = LabelCreationForm()
    context = home_page_context()
    context['form'] = form            

    return render(request, 'tasks/index.html', context)

#View, Change the completed page view when a task is deleted. 
def task_delete_completed_page(request, task_id):
    
    task = task_delete(request, task_id)
    
    #Context to be passsed to the completed page. 
    tasks_done = Tasks.objects.filter(task_status='Done')
    context = {'tasks_done': tasks_done}

    return render(request, 'tasks/completed_tasks.html', context)

#View, List of all completed tasks. 
def tasks_completed_list(request):

    tasks_done = Tasks.objects.filter(task_status='Done')
    context = {'tasks_done': tasks_done}

    return render(request, 'tasks/tasks_completed.html', context)

def task_open_completed_page(request, task_id):

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Open'
    task.task_last_updated_time = timezone.now()
    task.task_completed_time = None
    task.save()

    #Context to be passed to the home page
    form = LabelCreationForm()
    context = home_page_context()
    context['form'] = form            

    return render(request, 'tasks/index.html', context)

def label_delete(request, label_id):

    label = Labels.objects.get(id = label_id)
    label.label_status = 'Deleted'
    label.label_delete_time = timezone.now()
    label.save()

    #Context to be passed to the home page
    form = LabelCreationForm()
    context = home_page_context()
    context['form'] = form            

    return render(request, 'tasks/index.html', context)
   
def home_page_context():

    tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
    tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
    tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')
    tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
    
    label_list = Labels.objects.filter(label_status = 'Active')

    context = { 'tasks_not_done': tasks_not_done, 'tasks_in_progress': tasks_in_progress, 'label_list':label_list}
    
    return context

