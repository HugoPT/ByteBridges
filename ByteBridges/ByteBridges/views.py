from django.shortcuts import render


def Login(request):
    return render(request, "Login.html") 

def loginForm(request):
    return render(request, "loginForm.html") 

def IndexPage(request):
    return render(request, template_name='base_template.html') 

def dashboard(request):
    return render(request, template_name='dashboard.html') 

def Clients(request):
    return render(request, template_name='client.html')   






