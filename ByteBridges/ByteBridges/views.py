from django.shortcuts import render, redirect
from .models import Supplier
from django.db import connections


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
    # return redirect('dashboard')
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
        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_suppliers_create(%s,%s,%s,%s,%s,%s,%s,%s,)",
                           [name, nif, address, zipcode, city, phone, obs])
            # If the stored procedure returns results, you can fetch them
            result = cursor.fetchall()
            print(result)
        print(
            f"Inserted client " + name + " " + nif + " " + address + " " + zipcode + " " + city + " " + phone + " " + obs)
        # return render(request, 'your_template.html', {'result': result})
        return redirect('dashboard')
    # return the form
    return render(request, template_name='clientsCreate.html')


# Suppliers
def suppliersList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_suppliers_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        suppliers = [Supplier(*row) for row in result]
        return render(request,'suppliersList.html',{'suppliers': suppliers})


def suppliersCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        nif = request.POST.get('nif')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        obs = request.POST.get('obs')
        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_suppliers_create(%s,%s,%s,%s,%s,%s,%s,%s)",
                           [name, nif, address, zipcode, city, phone,email, obs])
            # If the stored procedure returns results, you can fetch them
            #result = cursor.fetchall()
            #print(result)
        print(f"Inserted supplier " + name + " " + nif + " " + address + " " + zipcode + " " + city + " " + phone + " " + email+ " " + obs)
        # return render(request, 'your_template.html', {'result': result})
        return redirect('dashboard')
    return render(request, template_name='suppliersCreate.html')


# orders
def createOrder(request):
    return render(request, template_name='createOrder.html')


def orderList(request):
    return render(request, template_name='orderList.html')
