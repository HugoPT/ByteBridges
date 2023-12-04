from django.shortcuts import render, redirect
from .models import Supplier, Warehouse, Client,Family


from django.db import connections


def Login(request):
    return render(request, "Login.html")


def loginForm(request):
    return render(request, "loginForm.html")


def IndexPage(request):
    return render(request, template_name='dashboard.html')

# Clients
def clientsList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_clients_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        clients = [Client(*row) for row in result]
        return render(request,'clientsList.html',{'clients':clients})

def clientsCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        individual = True
        nif = request.POST.get('nif')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        email = request.POST.get('email')
        obs = request.POST.get('obs')

        print(
            f"Inserted client {name} {nif} {address} {zipcode} {email} {city} {obs}")

        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_clients_create(%s,%s,%s,%s,%s,%s,%s,%s)",
                           [email,individual,zipcode,address,nif,name,obs,city])
            
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


#Family  sp_families_create
def familyCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_families_create(%s,%s)",
                           [name,desc])
  
        print(f"Inserted Family " + name + " " + desc)
        return redirect('dashboard')
    return render(request, template_name='familyCreate.html')

#Equipment
def createEquipment(request):
    
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_warehouses_list")
        result = cursor.fetchall()
       
        warehouse = [Warehouse(*row) for row in result]
        print(warehouse)
        
        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
       
        families = [Family(*row) for row in result]
        context={'warehouse':warehouse,'families':families}
    return render(request,'createEquipment.html',context=context)





    