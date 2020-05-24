from django.http import HttpResponse, HttpResponseRedirect
from .models import Tasks, Labels, TaskLogHours
from .forms import TaskCreationForm, TaskUpdationForm, LabelCreationForm, TaskLogHoursForm
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone

"""
There are 4 status of each task, which are self explanatory:
1. Open 
2. In Progress
3. Done
4. Delete 

The application has 5 main pages: 
1. Home Page to list all open and in progress tasks. 
2. Add / Edit task page to add and edit tasks. 
3. Completed Page to list all completed tasks. (Status = 'Done')
4. Log Hours page to log hours spent on each task. 
5. Task Summary page to have all task details at one place - task details and log hours. 

The user has to be logged in the application to access any of the pages. 
If user is not logged in, he / she will be redirected to the login page. 
If the user does not have an account, he / she will have to create an account on the register page. 
"""

def index(request):
    """Home page view of the application."""

    login_user = request.user
    if login_user.is_authenticated:  #explicit compare everywhere -> not to be done by conventions
        if request.method == 'POST': #create constants file, use that
            form = LabelCreationForm(request.POST)
            if form.is_valid(): #explicit compare            
                label = form.save(commit=False) #check whether space around =
                label.user = request.user
                label.label_create_time = timezone.now()
                label.save()
                    
                form = LabelCreationForm()
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

def task_add(request):
    """View to add a new task.
    The same page that is rendered in this view is shared by the edit task view.
    """

    login_user = request.user
    if login_user.is_authenticated:
        if request.method == 'POST':    
            form = TaskCreationForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.task_label = task.task_label.split("<QuerySet [",1)[1].split("]>")[0]
                task.task_label = task.task_label.replace("<Labels: ", "").replace(">","")
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

def task_edit(request, 
              task_id):
    """View to efit an existing task.
    The same page that is rendered in this view is shared by the add task view.
    """    
    
    login_user = request.user
    if login_user.is_authenticated:
        task = Tasks.objects.get(id = task_id)        
        if request.method == 'POST': 
            form = TaskUpdationForm(request.POST, instance = task)
            if form.is_valid():
                task = form.save(commit=False)
                task.task_label = task.task_label.split("<QuerySet [",1)[1].split("]>")[0]
                task.task_label = task.task_label.replace("<Labels: ", "").replace(">","")
                task.user = login_user
                task.task_last_updated_time = timezone.now()
                task.save()                
                return redirect('/tasks/')        
        else: 
            form = TaskUpdationForm(instance = task)        
        return render(request, 'tasks/task_edit.html', {'form': form})    
    else:
        return redirect('/tasks/login')


def task_complete(request, 
                  task_id):
    """Method that marks the status of a task as 'Done'. 
    This is called by other views. 
    """

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Done'
    task.task_last_updated_time = timezone.now()
    task.task_completed_time = timezone.now()
    task.save()
    return task

def task_complete_home_page(request, 
                            task_id):
    """View that marks a task as 'Done' on the home page."""

    login_user = request.user
    if login_user.is_authenticated:
        task = task_complete(request, task_id)        
        return redirect('/tasks/')
    else:
        return redirect('/tasks/login')

def task_inprogress(request, 
                    task_id):
    """View that marks an 'Open' task as 'In Progress' on the home page."""
    
    login_user = request.user
    if login_user.is_authenticated:
        task = Tasks.objects.get(id = task_id)
        task.task_status = 'In Progress'
        task.task_last_updated_time = timezone.now()
        task.save()
        return redirect('/tasks/')    
    else:
        return redirect('/tasks/login')

def task_delete(request, 
                task_id):
    """Method that marks a task as 'Delete'.
    This is called by other views.
    """

    task = Tasks.objects.get(id = task_id)
    task.task_status = 'Deleted'
    task.task_last_updated_time = timezone.now()
    task.save()
    return task    

def task_delete_home_page(request, 
                          task_id):
    """View that marks any task on Home Page as 'Delete'."""

    login_user = request.user
    if login_user.is_authenticated:    
        task = Tasks.objects.get(id = task_id)
        task = task_delete(request, task_id)
        return redirect('/tasks/')
    else:
        return redirect('/tasks/login')

def task_delete_completed_page(request, 
                               task_id):
    """View that marks any task on Completed Page as 'Delete'."""

    login_user = request.user
    if login_user.is_authenticated:
        task = task_delete(request, task_id)
        return redirect('/tasks/completed/')    
    else:
        return redirect('/tasks/login')

def tasks_completed_list(request):
    """Completed Page View of the Application."""

    login_user = request.user
    if login_user.is_authenticated:
        tasks_done = Tasks.objects.filter(task_status='Done')
        tasks_done = tasks_done.order_by('-task_completed_time')        
        login_user = request.user
        tasks_done = tasks_done.filter(user = login_user)
        context = {'tasks_done': tasks_done}
        return render(request, 'tasks/tasks_completed.html', context)    
    else:
        return redirect('/tasks/login')

def task_open_completed_page(request, 
                             task_id):
    """View that marks any task on the 'Completed' Page as 'Open'"""
    
    login_user = request.user
    if login_user.is_authenticated:
        task = Tasks.objects.get(id = task_id)
        task.task_status = 'Open'
        task.task_last_updated_time = timezone.now()
        task.task_completed_time = None
        task.save()
        return redirect('/tasks/')
    else:
        return redirect('/tasks/login')

def label_delete(request, 
                 label_id):
    """Method to delete a label from the Home Page."""

    login_user = request.user
    if login_user.is_authenticated:
        label = Labels.objects.get(id = label_id)
        label.label_status = 'Deleted'
        label.label_delete_time = timezone.now()
        label.save()
        return redirect('/tasks/')    
    else:
        return redirect('/tasks/login')

def home_page_context(request):
    """Method to determine the context to be passed for the home page template."""

    login_user = request.user

    tasks_not_done = Tasks.objects.exclude(task_status = 'Done')
    tasks_not_done = tasks_not_done.exclude(task_status = 'Deleted')
    tasks_not_done = tasks_not_done.exclude(task_status = 'In Progress')
    tasks_not_done = tasks_not_done.filter(user = login_user)
    
    tasks_in_progress = Tasks.objects.filter(task_status = 'In Progress')
    tasks_in_progress = tasks_in_progress.filter(user = login_user)
    
    label_list = Labels.objects.filter(label_status = 'Active')
    label_list = label_list.filter(user = login_user)

    date_today = timezone.now().date()

    context = {'tasks_not_done' : tasks_not_done, 'tasks_in_progress' : tasks_in_progress, 
               'label_list' : label_list, 'date_today' : date_today}    
    return context

def task_log_hours(request, 
                   task_id):
    """View to log hour corresponding to a task and add notes to it."""

    login_user = request.user
    if login_user.is_authenticated:        
        if request.method == 'POST': 
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

def task_log_summary(request, 
                     task_id):
    """View to log hours corresponding to a task and add notes to it."""

    login_user = request.user
    if login_user.is_authenticated:
        task_filtered = Tasks.objects.get(id = task_id)
        task_log_hours = TaskLogHours.objects.filter(task = task_filtered)
        return render(request, 'tasks/task_log_summary.html', 
                      {'task_log_hours':task_log_hours, 'task':task_filtered}) 
    else:
        redirect('/tasks/')
