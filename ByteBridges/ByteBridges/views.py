from django.shortcuts import render


def Login(request):
    return render(request, "Login.html") 

def loginForm(request):
    return render(request, "loginForm.html") 

def IndexPage(request):
    return render(request, template_name='dashboard.html') 

#def dashboard(request):
#   return render(request, template_name='dashboard.html') 


#Clients
def clientsList(request):
    return render(request, template_name='clientsList.html')   

def clientsCreate(request):
    return render(request, template_name='clientsCreate.html')   

#Suppliers
def suppliersList(request):
    return render(request, template_name='suppliersList.html')   

def suppliersCreate(request):
    return render(request, template_name='suppliersCreate.html')   

#orders
def createOrder(request):
    return render(request, template_name='createOrder.html')   

def orderList(request):
    return render(request, template_name='orderList.html')   








