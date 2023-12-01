from django.shortcuts import render, redirect
from .models import Supplier


def Login(request):
    return render(request, "Login.html")


def loginForm(request):
    return render(request, "loginForm.html")


def IndexPage(request):
    return render(request, template_name='dashboard.html')


# def dashboard(request):
#   return render(request, template_name='dashboard.html') 


# Clients
def clientsList(request):
    return render(request, template_name='clientsList.html')


def clientsCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        nif = request.POST.get('nif')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        obs = request.POST.get('obs')

        print(f"Inserted client " + name + nif + address + zipcode + city + phone + obs)

        return redirect('dashboard')
    # return the form
    return render(request, template_name='clientsCreate.html')


# Suppliers
def suppliersList(request):
    return render(request, template_name='suppliersList.html')


def suppliersCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        nif = request.POST.get('nif')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        obs = request.POST.get('obs')
        s = Supplier(
            name=name,
            nif=nif,
            email=email,
            address=address,
            zipcode=zipcode,
            city=city,
            phone=phone,
            obs=obs
        )
        s.save()
        print(
            f"Inserted Supplier " + name + " " + nif + " " + address + " " + zipcode + " " + city + " " + phone + " " + obs)
        return redirect('dashboard')
    return render(request, template_name='suppliersCreate.html')


# orders
def createOrder(request):
    return render(request, template_name='createOrder.html')


def orderList(request):
    return render(request, template_name='orderList.html')
