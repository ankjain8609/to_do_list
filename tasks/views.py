from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Tasks, Labels, TaskLogHours
from .forms import TaskCreationForm, TaskUpdationForm, LabelCreationForm, TaskLogHoursForm
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.models import User

#View, Home Page
def index(request):
    user = request.user
    if user.is_authenticated:
    #Check if the user is authenticated.    
        if request.method == "POST":
        #Label Creation Form    
            form = LabelCreationForm(request.POST)
            
            if form.is_valid():
            
                label = form.save(commit=False)
                label.user = request.user
                label.label_create_time = timezone.now()
                label.save()
                    
                form = LabelCreationForm()
                #Set of parameters that need to be passed in the home page template.
                context = home_page_context(request) 
                context['form'] = form
                
                return render(request, 'tasks/index.html', context)
        else:

            form = LabelCreationForm()
            context = home_page_context(request)
            context['form'] = form
            
            return render(request, 'tasks/index.html', context)
    else:
        return redirect('/tasks/login')

#View, Add Task
def task_add(request):
    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.    

        if request.method == "POST":
        #Task Creation Form       
            form = TaskCreationForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.task_label = task.task_label.split("<QuerySet [",1)[1].split("]>")[0].replace("<Labels: ", "").replace(">","")
                task.task_status = 'Open'
                task.task_create_time = timezone.now()
                task.task_last_updated_time = timezone.now()
                task.save()
                
                return redirect('/tasks/')

        else:
            form = TaskCreationForm()
        
        return render(request, 'tasks/task_edit.html', {'form': form})
    
    else:
        return redirect('/tasks/login')

#View, Edit Task
def task_edit(request, task_id):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.  

        task = Tasks.objects.get(id = task_id)
        
        if request.method == "POST": 
        #Task Updation Form
            form = TaskUpdationForm(request.POST, instance = task)

            if form.is_valid():
                task = form.save(commit=False)
                task.task_label = task.task_label.split("<QuerySet [",1)[1].split("]>")[0].replace("<Labels: ", "").replace(">","")
                task.user = request.user
                task.task_last_updated_time = timezone.now()
                task.save()                
                return redirect('/tasks/')
        
        else: 
            form = TaskUpdationForm(instance = task)
        
        return render(request, 'tasks/task_edit.html', {'form': form})    
    
    else:
        return redirect('/tasks/login')

def task_log_hours(request, task_id):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.  
        
        if request.method == "POST": 
        #Task Updation Form
            form = TaskLogHoursForm(request.POST)
            task = Tasks.objects.get(id = task_id)

            if form.is_valid():
                task_log_hours = form.save(commit=False)
                task_log_hours.user = request.user
                task_log_hours.task = task
                task_log_hours.task_log_time = timezone.now()
                task_log_hours.save()
                return redirect('/tasks/')
        
        else:
            form = TaskLogHoursForm()
        
        return render(request, 'tasks/task_log_hours.html', {'form': form})

    else:
        return redirect('/tasks/login')    

def task_log_summary(request, task_id):
    user = request.user
    if user.is_authenticated:
        task_filtered = Tasks.objects.get(id = task_id)
        task_log_hours = TaskLogHours.objects.filter(task = task_filtered)
        return render(request, 'tasks/task_log_summary.html', {'task_log_hours':task_log_hours, 'task':task_filtered}) 
    else:
        redirect('/tasks/')

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

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.  
        task = task_complete(request, task_id)        
        return redirect('/tasks/')
 
    else:
        return redirect('/tasks/login')


#View, Change the home page view when a task is marked as in progress.
def task_inprogress(request, task_id):
    
    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.      
        task = Tasks.objects.get(id = task_id)
        task.task_status = 'In Progress'
        task.task_last_updated_time = timezone.now()
        task.save()
        return redirect('/tasks/')
    
    else:
        return redirect('/tasks/login')

#Controller, Mark Task Status as deleted 
def task_delete(request, task_id):

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Deleted'
    task.task_last_updated_time = timezone.now()
    task.save()
    return task    

#View, Change the home page view when a task is deleted. 
def task_delete_home_page(request, task_id):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.      
    
        task = Tasks.objects.get(id = task_id)
        task = task_delete(request, task_id)
        return redirect('/tasks/')
    
    else:
        return redirect('/tasks/login')

#View, Change the completed page view when a task is deleted. 
def task_delete_completed_page(request, task_id):
    
    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.      

        task = task_delete(request, task_id)
        return redirect('/tasks/completed/')
    
    else:
        return redirect('/tasks/login')

#View, List of all completed tasks. 
def tasks_completed_list(request):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.
    
        tasks_done = Tasks.objects.filter(task_status='Done').order_by('-task_completed_time')        
        login = request.user
        tasks_done = tasks_done.filter(user = login)
        context = {'tasks_done': tasks_done}
        return render(request, 'tasks/tasks_completed.html', context)
    
    else:
        return redirect('/tasks/login')

def task_open_completed_page(request, task_id):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.

        task = Tasks.objects.get(id = task_id)
        task.task_status = 'Open'
        task.task_last_updated_time = timezone.now()
        task.task_completed_time = None
        task.save()
        return redirect('/tasks/')
    
    else:
        return redirect('/tasks/login')

def label_delete(request, label_id):

    user = request.user
    if user.is_authenticated:
    #Check of the user is authenticated.

        label = Labels.objects.get(id = label_id)
        label.label_status = 'Deleted'
        label.label_delete_time = timezone.now()
        label.save()
        return redirect('/tasks/')
    
    else:
        return redirect('/tasks/login')

#Controlled, Passing the latest context of tasks and label lists on the home page.  
def home_page_context(request):

    login = request.user
    tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
    tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
    tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')
    tasks_not_done = tasks_not_done.filter(user = login)
    
    tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
    tasks_in_progress = tasks_in_progress.filter(user = login)
    
    label_list = Labels.objects.filter(label_status = 'Active').filter(user = login)
    date_today = timezone.now().date()

    context = { 'tasks_not_done': tasks_not_done, 'tasks_in_progress': tasks_in_progress, 'label_list':label_list, 'date_today' : date_today}
    
    return context
