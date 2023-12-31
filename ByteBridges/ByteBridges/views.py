import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Warehouse, Client, Family, ArticleType, ComponentListFamily, User, Category, Labor, Terms, \
    Stock, Sales
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.http import JsonResponse
import json


def Homepage(request):
    return render(request, "Home.html")


@login_required
def IndexPage(request):
    return render(request, template_name='dashboard.html')


# Clients
@login_required
def clientList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("SELECT * FROM view_clients_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        clients = [Client(*row) for row in result]
        return render(request, 'clientList.html', {'clients': clients})


@login_required
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


@login_required
def clientEdit(request, client_id):
    # Fetch the client information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_clients_list WHERE idclient = %s", [client_id])
        client = cursor.fetchone()

    if request.method == 'POST':
        # Get the data from the form
        email = request.POST.get('email')
        individual = request.POST.get('individual') == 'True'
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        nif = request.POST.get('nif')
        name = request.POST.get('name')
        description = request.POST.get('obs')
        city = request.POST.get('city')
        eletronicinvoice = request.POST.get('eletronicinvoice') == 'True'

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_clients_update(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [client_id, email, individual, zipcode, address, nif, name, description, city,
                            eletronicinvoice])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('clientList')

    return render(request, 'clientEdit.html', {'client_id': client_id,
                                               'client': {'email': client[1], 'individual': client[2],
                                                          'zipcode': client[3], 'address': client[4], 'nif': client[5],
                                                          'name': client[6], 'description': client[7],
                                                          'city': client[8], 'eletronicinvoice': client[9]}})


@login_required
def clientDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            client_id = request.POST['id']
            cursor.execute("CALL sp_clients_delete(%s)", [client_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('clientList')


@login_required
def orderClientList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("SELECT * FROM view_sales_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        sales = [Sales(*row) for row in result]

    return render(request, 'orderClientList.html', {'sales': sales})


@login_required
def orderClientCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_equipments_list2")
        toSell = cursor.fetchall()

        cursor.execute("SELECT * FROM view_clients_list", [])
        resultClient = cursor.fetchall()
        clients = [Client(*row) for row in resultClient]

        if request.method == 'POST':
            client_id = request.POST.get('client')
            rows_data = json.loads(request.POST.get('rows'))
            observations = request.POST.get('observations')

            # Create order client
            cursor.execute("SELECT fn_ordersclient_create(CAST(%s AS INTEGER), %s)", [client_id, observations])
            idorderclient = cursor.fetchone()
            if idorderclient:
                for row in rows_data:
                    cursor.execute("CALL sp_sales_create(%s,%s,%s)", [idorderclient[0], row['id'], row['quantity']])

                return JsonResponse({'status': 'success'})

    context = {'toSell': toSell, 'clients': clients}
    return render(request, 'orderClientCreate.html', context)


@login_required
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


@login_required
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


@login_required
def supplierEdit(request, idsupplier):
    # Fetch the supplier information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_suppliers_list WHERE idsupplier = %s", [idsupplier])
        supplier = cursor.fetchone()

    if not supplier:
        # If the supplier is not found, handle it accordingly (e.g., return a 404 or display an error message)
        return render(request, 'supplierEdit.html', {'supplier_not_found': True})

    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        nif = request.POST.get('nif')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        obs = request.POST.get('obs')

        # Print the data before updating the supplier
        print("Data before update:")
        print(
            f"Name: {name}, NIF: {nif}, Address: {address}, Zipcode: {zipcode}, City: {city}, Phone: {phone}, Email: {email}, Observations: {obs}")

        # Call the stored procedure to update the supplier
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_suppliers_update(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [idsupplier, name, nif, address, zipcode, city, phone, email, obs])
            # Commit the changes to the database

        # Always return a JsonResponse for AJAX requests
        return JsonResponse({'status': 'success'})

    return render(request, 'supplierEdit.html', {'idsupplier': idsupplier,
                                                 'supplier': {'name': supplier[1], 'nif': supplier[2],
                                                              'address': supplier[3], 'zipcode': supplier[4],
                                                              'city': supplier[5],
                                                              'phone': supplier[6], 'email': supplier[7],
                                                              'obs': supplier[8]}})


@login_required
def supplierDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        with connections['admin'].cursor() as cursor:
            supplier_id = request.POST['id']
            cursor.execute("CALL sp_suppliers_delete(%s)", [supplier_id])
            return JsonResponse({'status': 'success'})

        return redirect('supplierList')


@login_required
def orderSupplierList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_buy_list_supplier", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()

        return render(request, 'orderSupplierList.html', {'orders': result})


@csrf_exempt
@login_required
def orderSupplierLinesFetch(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("SELECT * FROM fn_orderssuplier_getlines(%s);", [id])
        list = cursor.fetchall()
        print(list)
        return JsonResponse({'list': list})


@login_required
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
                        cursor.execute("CALL sp_purchases_create(%s,%s,%s)",
                                       [result[0],
                                        item['component'],
                                        item['quantity']])
                return JsonResponse({'status': 'success'})
    return render(request, template_name='orderSupplierCreate.html', context=context)


@login_required
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




@login_required
def documentsSupplier(request):
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

        cursor.execute("select * from view_terms_list")
        result = cursor.fetchall()
        terms_list = [Terms(*row) for row in result]

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        families = [Family(*row) for row in result]

        context = {'suppliers': suppliers, 'terms_list': terms_list, 'warehouses': warehouses, 'families': families,
                   'docNumber': docNumber}

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
    return render(request, template_name='documentsSupplier.html', context=context)


# todo fix this csrf
@csrf_exempt
@login_required
def documentsSupplierFetch(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("select * from fn_pendingSuppliersOrders(%s);", [id[0]])
        list = cursor.fetchall()
        return JsonResponse({'list': list})


# todo fix this csrf
@csrf_exempt
@login_required
def documentsSupplierLinesFetch(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("SELECT * FROM fn_orderssuplier_getlines(%s);", [id])
        list = cursor.fetchall()
        print(list)
        return JsonResponse({'list': list})


@csrf_exempt
@login_required
def documentsSupplierRegisterInvoice(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        supplier = request.POST.get('supplier')
        invoice_type = request.POST.get('invoice_type')
        invoice_number = request.POST.get('invoice_number')
        invoice_value = request.POST.get('invoice_value')
        invoice_date = request.POST.get('invoice_date')
        payment_type = request.POST.get('payment_type')

        documentLines = json.loads(request.POST.get('documentLines'))
        related_document_id = request.POST.get('related_document_id')
        obs = request.POST.get('obs')

        cursor.execute("select fn_generate_ordersSupplier_invoice(%s,%s,%s,%s,%s,%s);",
                       [payment_type, related_document_id, obs, invoice_type, invoice_number, invoice_date])
        doc = cursor.fetchone()

        for line in documentLines:
            cursor.execute("CALL  sp_lines_create(%s,%s,%s);", [doc[0], line[0], line[6]])
        return JsonResponse({'list': related_document_id})


@csrf_exempt
@login_required
def documentsSupplierRegisterInvoiceLines(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("SELECT * FROM fn_orderssuplier_getlines(%s);", [id])
        list = cursor.fetchall()
        print(list)
        return JsonResponse({'list': list})


@login_required
def productionEquipmentCreate(request, equipment_id):
    with connections['admin'].cursor() as cursor:

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        families = [Family(*row) for row in result]

    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))
        for item in data:
            with connections['admin'].cursor() as cursor:
                cursor.execute("CALL sp_productionitems_add(%s,%s,%s)",
                               [equipment_id,
                                item['component'],
                                item['quantity']])
        return JsonResponse({'status': 'success'})
    return render(request, 'productionEquipmentCreate.html', {'families': families, 'equipment_id': equipment_id})


@login_required
def familyList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_families_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        families = [Family(*row) for row in result]
        return render(request, 'familyList.html', {'families': families})


@login_required
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


@login_required
def familyEdit(request, family_id):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_families_list WHERE idfamily = %s", [family_id])
        family = cursor.fetchone()

    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Call the stored procedure to update the family
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_families_update(%s, %s, %s)", [family_id, name, description])
            # Commit the changes to the database

        return redirect('familyList')

    return render(request, 'familyEdit.html',
                  {'idfamily': family_id, 'family': {'name': family[1], 'description': family[2]}})


@login_required
def familyDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            family_id = request.POST['id']
            cursor.execute("CALL sp_families_delete(%s)", [family_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('familyList')


@login_required
def equipmentList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_equipments_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        equipments = [ArticleType(*row) for row in result]
        return render(request, 'equipmentList.html', {'equipments': equipments})


@login_required
def equipmentCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_categories_list")
        result = cursor.fetchall()
        category = [Category(*row) for row in result]
        context = {'category': category}

    if request.method == 'POST':
        name = request.POST.get('name')
        idfamily = None
        idcategory = request.POST.get('category')
        description = request.POST.get('description')
        image = ""
        profit_margin = 0
        barcode = request.POST.get('barcode')
        reference = request.POST.get('reference')

        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_articletypes_create(%s, %s, %s, %s, %s, %s, %s, %s)",
                           [idfamily, idcategory, name, description, image, profit_margin, barcode, reference])
            return redirect('dashboard')

    return render(request, 'equipmentCreate.html', context=context)


@login_required
def productionEquipmentEdit(request, equipment_id):
    with connections['admin'].cursor() as cursor:

        cursor.execute("SELECT * FROM fn_productionitems_get (%s);", [equipment_id])
        equipment = cursor.fetchall()

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        families = [Family(*row) for row in result]

    if request.method == 'POST':
        data = json.loads(request.POST.get('data'))
        for item in data:
            with connections['admin'].cursor() as cursor:
                cursor.execute("CALL sp_productionitems_update(%s,%s,%s)",
                               [equipment_id,
                                item['component'],
                                item['quantity']])
        return JsonResponse({'status': 'success'})
    return render(request, 'productionEquipmentEdit.html', {'families': families, 'equipment_id': equipment_id,
                                                            'equipment': equipment})


@login_required
def equipmentEdit(request, equipment_id):
    # Fetch the client information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_equipments_list WHERE idarticletype = %s", [equipment_id])
        equipment = cursor.fetchone()

        cursor.execute("select * from view_categories_list")
        result = cursor.fetchall()
        category = [Category(*row) for row in result]

    if request.method == 'POST':
        name = request.POST.get('name')
        idfamily = None
        idcategory = request.POST.get('idcategory')
        description = request.POST.get('description')
        image = ""
        profit_margin = 0
        barcode = request.POST.get('barcode')
        reference = request.POST.get('reference')

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_articletypes_update(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [equipment_id, idfamily, idcategory, name, description, image, profit_margin, barcode,
                            reference])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('equipmentList')

    return render(request, 'equipmentEdit.html', {'equipment_id': equipment_id, 'category': category,
                                                  'equipment': {'name': equipment[1], 'category': equipment[3],
                                                                'description': equipment[4], 'barcode': equipment[6],
                                                                'reference': equipment[7]}})


@login_required
def equipmentDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            equipment_id = request.POST['id']
            cursor.execute("CALL sp_articletypes_delete(%s)", [equipment_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('equipmentList')


@login_required
def componentList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_components_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()

        components = [ArticleType(*row) for row in result]
        return render(request, 'componentList.html', {'components': components})


@login_required
def componentCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()

        family = [Family(*row) for row in result]
        context = {'family': family}

    if request.method == 'POST':
        name = request.POST.get('name')
        idfamily = request.POST.get('family')
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


@login_required
def componentEdit(request, component_id):
    # Fetch the client information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_components_list WHERE idarticletype = %s", [component_id])
        component = cursor.fetchone()

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        family = [Family(*row) for row in result]

    if request.method == 'POST':
        name = request.POST.get('name')
        idfamily = request.POST.get('idfamily')
        idcategory = None
        description = request.POST.get('description')
        image = ""
        profit_margin = int(request.POST.get('profitmargin')) / 100
        barcode = request.POST.get('barcode')
        reference = request.POST.get('reference')

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_articletypes_update(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [component_id, idfamily, idcategory, name, description, image, profit_margin, barcode,
                            reference])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('componentList')

    return render(request, 'componentEdit.html', {'component_id': component_id, 'family': family,
                                                  'component': {'name': component[1], 'family': component[2],
                                                                'description': component[4],
                                                                'profitmargin': int(component[5] * 100),
                                                                'barcode': component[6],
                                                                'reference': component[7]}})


@login_required
def componentDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            component_id = request.POST['id']
            cursor.execute("CALL sp_articletypes_delete(%s)", [component_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('componentList')


@login_required
def stockList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_getstock_equipments")
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        equipments = [Stock(*row) for row in result]

        cursor.execute("select  * from view_getstock_components")
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()

        components = [Stock(*row) for row in result]

        context = {'equipments': equipments, 'components': components}

        return render(request, 'stockList.html', context=context)


@login_required
def laborList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("SELECT * FROM view_labors_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        labors = [Labor(*row) for row in result]
        return render(request, 'laborList.html', {'labors': labors})


@login_required
def laborCreate(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        hourrate = request.POST.get('hourrate')

        print(
            f"Inserted labor {name} {hourrate}")

        with connections['admin'].cursor() as cursor:
            # Call the stored procedure using the CALL statement
            cursor.execute("CALL sp_labors_create(%s,%s)",
                           [name, hourrate])

        return redirect('dashboard')

    # return the form
    return render(request, template_name='laborCreate.html')


@login_required
def laborEdit(request, labor_id):
    # Fetch the client information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_labors_list WHERE idlabor = %s", [labor_id])
        labor = cursor.fetchone()

    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        hourrate = request.POST.get('hourrate')

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_labors_update(%s, %s, %s)",
                           [labor_id, name, hourrate])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('laborList')

    return render(request, 'laborEdit.html', {'labor_id': labor_id,
                                              'labor': {'name': labor[1], 'hourrate': labor[2]}})


@login_required
def laborDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            labor_id = request.POST['id']
            cursor.execute("CALL sp_labors_delete(%s)", [labor_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('laborList')


@login_required
def userList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("SELECT * FROM view_users_list", [])
        # If the stored procedure returns results, you can fetch them
        result = cursor.fetchall()
        print(result)
        users = [User(*row) for row in result]
        return render(request, 'userList.html', {'users': users})


@login_required
def userEdit(request, user_id):
    # Fetch the client information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM view_users_list WHERE iduser = %s", [user_id])
        user = cursor.fetchone()

    if request.method == 'POST':
        # Get the data from the form
        idrole = request.POST.get('role')
        idlabor = request.POST.get('labor')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_users_update(%s, %s, %s, %s, %s, %s)",
                           [user_id, idrole, idlabor, email, password, name])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('userList')

    return render(request, 'userEdit.html', {'user_id': user_id,
                                             'user': {'name': user[1], 'password': user[3],
                                                      'email': user[2], 'labor': user[5],
                                                      'role': user[4]}})


@login_required
def userDelete(request):
    if request.method == 'POST' and 'id' in request.POST:
        # Call the stored procedure to delete the client
        with connections['admin'].cursor() as cursor:
            user_id = request.POST['id']
            cursor.execute("CALL sp_users_delete(%s)", [user_id])
            return JsonResponse({'status': 'success'})
        # Redirect to the client list page after deletion
        return redirect('userList')




