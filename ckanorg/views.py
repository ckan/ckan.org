from django.shortcuts import render

def not_found(request):
    return render(request, "404.html")

def server_error(request):
    return render(request, "500.html")
