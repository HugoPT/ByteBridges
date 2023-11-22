from django.shortcuts import render



def IndexPage(request):
    return render(request, template_name='base_template.html')  






