from django.shortcuts import render


def Login(request):
    return render(request, "Login.html") 

def IndexPage(request):
    return render(request, template_name='base_template.html') 


def Clients(request):
    return render(request, template_name='dashboard.html')   






