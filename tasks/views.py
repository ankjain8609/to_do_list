from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Tasks
from .forms import TaskCreationForm
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    all_tasks_list = Tasks.objects.all()
    context = {'all_tasks_list': all_tasks_list}
    return render(request, 'tasks/index.html', context)

def add_task(request):
    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_create_time = timezone.now()
            task.task_last_updated_time = timezone.now()
            task.save()
            
            all_tasks_list = Tasks.objects.all()
            context = {'all_tasks_list': all_tasks_list}
            return render(request, 'tasks/index.html', context)
    else:
        form = TaskCreationForm()
    return render(request, 'tasks/add_task.html', {'form': form})
