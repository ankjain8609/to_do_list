from django.http import HttpResponse
def index(request):
    return HttpResponse("Home Page for creating and managing tasks.")