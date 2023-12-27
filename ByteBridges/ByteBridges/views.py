import datetime

from django.shortcuts import render, redirect,get_object_or_404
from .models import Supplier, Warehouse, Client, Family, Article, ArticleType, Equipment, ComponentListFamily

from django.db import connections
from django.http import JsonResponse
import json


def Login(request):
    return render(request, "Login.html")


def loginForm(request):
    return render(request, "loginForm.html")


def IndexPage(request):
    return render(request, template_name='dashboard.html')


# Clients
def clientList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("SELECT * FROM view_clients_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        clients = [Client(*row) for row in result]
        return render(request, 'clientList.html', {'clients': clients})


def clientCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        individual = True
        nif = request.POST.get('nif')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        email = request.POST.get('email')
        obs = request.POST.get('obs')
        eletronicinvoice = True

        print(
            f"Inserted client {name} {nif} {address} {zipcode} {email} {city} {obs}")

        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_clients_create(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           [email, individual, zipcode, address, nif, name, obs, city, eletronicinvoice])

        return redirect('dashboard')

    # return the form
    return render(request, template_name='clientCreate.html')

def clientEdit(request, client_id):

    if request.method == 'POST':
        # Get the data from the form
        email = request.POST.get('email')
        individual = request.POST.get('individual') == 'True'
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        nif = request.POST.get('nif')
        name = request.POST.get('name')
        description = request.POST.get('description')
        city = request.POST.get('city')
        eletronicinvoice = request.POST.get('eletronicinvoice') == 'True'

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_clients_update(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [client_id, email, individual, zipcode, address, nif, name, description, city, eletronicinvoice])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('clientList')

    return render(request, 'clientEdit.html', {'client_id': client_id})


def clientConfirmationDelete(request, client_id):
    # Assuming you have a 'clientConfirmationDelete.html' template
    return render(request, 'clientConfirmationDelete.html', {'client_id': client_id})

def clientDelete(request, client_id):
    if request.method == 'POST':
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_clients_delete(%s)", [client_id])
            # Commit the changes to the database

        # Redirect to the client list page after deletion
        return redirect('clientList')


def orderClientList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_suppliers_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        suppliers = [Supplier(*row) for row in result]
        return render(request, 'orderClientList.html', {'suppliers': suppliers})


def orderClientCreate(request):
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
                           [name, nif, address, zipcode, city, phone, email, obs])
            # If the stored procedure returns results, you can fetch them
            # result = cursor.fetchall()
            # print(result)
        print(
            f"Inserted supplier " + name + " " + nif + " " + address + " " + zipcode + " " + city + " " + phone + " " + email + " " + obs)
        # return render(request, 'your_template.html', {'result': result})
        return redirect('dashboard')
    return render(request, template_name='orderClientCreate.html')


# Suppliers
def supplierList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_suppliers_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        suppliers = [Supplier(*row) for row in result]
        return render(request, 'supplierList.html', {'suppliers': suppliers})



def supplierCreate(request):
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
                           [name, nif, address, zipcode, city, phone, email, obs])
            # If the stored procedure returns results, you can fetch them
            # result = cursor.fetchall()
            # print(result)
        print(
            f"Inserted supplier " + name + " " + nif + " " + address + " " + zipcode + " " + city + " " + phone + " " + email + " " + obs)
        # return render(request, 'your_template.html', {'result': result})
        return redirect('dashboard')
    return render(request, template_name='supplierCreate.html')


def supplierConfirmationDelete(request, supplier_id):
    # Assuming you have a 'clientConfirmationDelete.html' template
    return render(request, 'supplierConfirmationDelete.html', {'supplier_id': supplier_id})

def supplierDelete(request, supplier_id):
    if request.method == 'POST':
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_suppliers_delete(%s)", [supplier_id])
            # Commit the changes to the database

        # Redirect to the client list page after deletion
        return redirect('supplierList')


def orderSupplierList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_suppliers_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        suppliers = [Supplier(*row) for row in result]
        return render(request, 'orderSupplierList.html', {'suppliers': suppliers})


def orderSupplierCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_suppliers_list")
        result = cursor.fetchall()
        docNumber = [Supplier(*row) for row in result]

        cursor.execute("select * from view_suppliers_list")
        result = cursor.fetchall()
        suppliers = [Supplier(*row) for row in result]

        cursor.execute("select * from view_warehouses_list")
        result = cursor.fetchall()
        warehouses = [Warehouse(*row) for row in result]

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        families = [Family(*row) for row in result]

        context = {'suppliers': suppliers, 'warehouses': warehouses, 'families': families, 'docNumber': docNumber}

    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))
        header = json.loads(request.POST.get('header'))
        # create a new supplier enc header
        with connections['admin'].cursor() as cursor:
            cursor.execute("select fn_orderssupplier_create(%s,%s,%s)",
                           [header[0]['obs'], header[0]['idsupplier'], header[0]['idwarehouse']])
            result = cursor.fetchone()
            if result:
                for item in data:
                    with connections['admin'].cursor() as cursor:
                        cursor.execute("CALL sp_buy_create(%s,%s,%s)",
                                       [result[0],
                                        item['component'],
                                        item['quantity']])
                return JsonResponse({'status': 'success'})
    return render(request, template_name='orderSupplierCreate.html', context=context)


def get_articles(request):
    print(request)
    if request.method == 'GET':
        family_id = request.GET.get('family_id')

        with connections['admin'].cursor() as cursor:
            cursor.execute("SELECT * FROM fn_components_list_family(CAST(%s AS INTEGER))", [family_id])
            result = cursor.fetchall()
            print(result)
            articles = [ComponentListFamily(*row) for row in result]

        # Convert ComponentListFamily objects to dictionaries
        articles_data = [{'idarticle': article.at_id, 'name': article.at_name} for article in articles]
        print(articles_data)

        data = {'articles': articles_data}
        print(data)
        return JsonResponse(data)


# Family  sp_families_create
def familyCreate(request):
    with connections['admin'].cursor() as cursor:
        if request.method == 'POST':
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            with connections['admin'].cursor() as cursor:
                # Call the stored procedure using the CALL statement
                cursor.execute("CALL sp_families_create(%s,%s)",
                            [name, desc])

            print(f"Inserted Family " + name + " " + desc)
            return redirect('dashboard')
        return render(request, template_name='familyCreate.html')

def familyEdit(request):  
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_families_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        families = [Family(*row) for row in result]
        context = {'families': families}
        
        if request.method == 'POST' and 'id' in request.POST:
            p_id = request.POST['id']
            cursor.execute("Call sp_families_delete(%s)", [p_id])
            return JsonResponse({'status': 'success'})
        return render(request, 'familyEdit.html', context=context)


# Equipment
def equipmentCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_warehouses_list")
        result = cursor.fetchall()

        warehouse = [Warehouse(*row) for row in result]
        print(warehouse)

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()

        families = [Family(*row) for row in result]
        context = {'warehouse': warehouse, 'families': families}

    return render(request, 'equipmentCreate.html', context=context)


def equipmentList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_equipments_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        equipments = [Equipment(*row) for row in result]
        context = {'equipments': equipments}
        return render(request, 'equipmentList.html', context=context)


def componentCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()

        families = [Family(*row) for row in result]
        context = {'families': families}

    if request.method == 'POST':
        name = request.POST.get('name')
        idfamily = request.POST.get('idfamily')
        idcategory = None
        description = request.POST.get('description')
        image = ""
        profit_margin = int(request.POST.get('profitmargin')) / 100
        barcode = request.POST.get('barcode')
        reference = request.POST.get('reference')

        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_articletypes_create(%s, %s, %s, %s, %s, %s, %s, %s)",
                           [idfamily, idcategory, name, description, image, profit_margin, barcode, reference])
            return redirect('dashboard')

    return render(request, 'componentCreate.html', context=context)


def componentList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_articletypes_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()

        return render(request, 'componentList.html', {'result': result})


def supplierEdit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    return render(request, 'supplierEdit.html', {'supplier': supplier})