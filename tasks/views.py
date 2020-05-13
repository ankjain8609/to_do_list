from django.http import HttpResponse
from .models import Tasks
from django.shortcuts import render

def index(request):
    all_tasks_list = Tasks.objects.all()
    context = {'all_tasks_list': all_tasks_list}
    return render(request, 'tasks/index.html', context)
