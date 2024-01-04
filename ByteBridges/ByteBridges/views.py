import datetime
from django.shortcuts import render, redirect
from .models import Supplier, Warehouse, Client, Family, ArticleType, ComponentListFamily, User, Category, Labor, Terms, \
    Stock, ClientBuyList, Tecnician, EquipmentsItems, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connections
from django.http import JsonResponse, HttpResponse
import json
from django.core.serializers import serialize
from django.conf import settings
from django import template
import pymongo

def group_required(group_name):
    def in_group(user):
        if user.groups.filter(name=group_name).exists():
            return True
        return False
    return user_passes_test(in_group, login_url='/dashboard')

def Homepage(request):
    return render(request, "Home.html")


@csrf_exempt
def logout(request):
    return render(request, "home.html")


@login_required
def IndexPage(request):
    user_groups = request.user.groups.all()
    user_role = user_groups[0] if user_groups else None
    if user_role == "Técnico":
        return render(request, 'xxx.html', {'user_role': user_role})
    else:
        return render(request, 'dashboard.html', {'user_role': user_role})


# Clients
@login_required
@group_required('Administrador')
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
        cursor.execute("SELECT * FROM view_buy_list_clients", [])
        result = cursor.fetchall()

        sales = []
        for row in result:
            iddocument, documentnumber, name, date_str, duedate_str, status = row
            date = datetime.datetime.strptime(date_str, '%d-%m-%Y').date()
            duedate = datetime.datetime.strptime(duedate_str, '%d-%m-%Y').date()
            sales.append(ClientBuyList(iddocument, documentnumber, name, date, duedate, status))

        print("aaaaaaaaaaa", sales)

    return render(request, 'orderClientList.html', {'sales': sales})


@csrf_exempt
@login_required
def orderClientLinesFetch(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("SELECT * FROM fn_ordersClient_getLines(%s);", [id])
        list = cursor.fetchall()
        print(list)
        return JsonResponse({'list': list})


@csrf_exempt
@login_required
def orderClientFetchInvoice(request, idorder):
    # Fetch the supplier information from the database
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM fn_ordersClient_getinvoice(%s);", [idorder])
        invoice = cursor.fetchone()

        cursor.execute("SELECT * FROM fn_ordersClient_getLines(%s);", [idorder])
        order = cursor.fetchall()

        cursor.execute("SELECT * FROM fn_invoice_getTotal(%s);", [idorder])
        total = cursor.fetchone()

        return render(request, 'orderClientInvoiceDetails.html', {'idorder': idorder,
                                                                  'order': order,
                                                                  'total': {'total': total[0]},
                                                                  'invoice':
                                                                      {'document': invoice[0],
                                                                       'date': invoice[1],
                                                                       'client': invoice[3],
                                                                       'email': invoice[4],
                                                                       'obs': invoice[5],
                                                                       }})


@login_required
def orderClientCreate(request):
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_equipments_list2")
        toSell = cursor.fetchall()

        cursor.execute("SELECT * FROM view_clients_list", [])
        resultClient = cursor.fetchall()
        clients = [Client(*row) for row in resultClient]

        cursor.execute("SELECT * FROM view_terms_list", [])
        resultTerms = cursor.fetchall()
        terms = [Terms(*row) for row in resultTerms]

        if request.method == 'POST':
            client_id = request.POST.get('client')
            term_id = request.POST.get('term')
            rows_data = json.loads(request.POST.get('rows'))
            observations = request.POST.get('observations')
            print("client_id:", client_id)
            print("term_id:", term_id)

            # Create order client
            cursor.execute("SELECT fn_ordersclient_create(CAST(%s AS INTEGER), %s, CAST(%s AS INTEGER))",
                           [client_id, observations, term_id])
            idorderclient = cursor.fetchone()
            if idorderclient:
                for row in rows_data:
                    print("Row:", row)
                    cursor.execute("CALL sp_sales_create(%s,%s,%s)", [idorderclient[0], row['id'], row['quantity']])

                return JsonResponse({'status': 'success'})

    context = {'toSell': toSell, 'clients': clients, 'terms': terms}
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
        orders = cursor.fetchall()

        cursor.execute("select * from view_suppliers_list")
        result = cursor.fetchall()
        suppliers = [Supplier(*row) for row in result]

        return render(request, 'orderSupplierList.html', {'orders': orders, 'suppliers': suppliers})


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


@csrf_exempt
@login_required
def orderSupplierExportJson(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        id = request.POST.get('id')
        cursor.execute("SELECT * FROM fn_export_orderssupplier_and_lines(%s);", [id])
        jsonexport = cursor.fetchall()
        print(jsonexport)
        return JsonResponse({'jsonexport': jsonexport})


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


# get Components for lines table
@login_required
def get_items(request):
    if request.method == 'GET':
        equipment_id = request.GET.get('equipment_id')
        if equipment_id and equipment_id.isdigit():
            with connections['admin'].cursor() as cursor:
                cursor.execute("SELECT * FROM fn_productionitems_get(CAST(%s AS INTEGER))", [equipment_id])
                result = cursor.fetchall()
                items = [EquipmentsItems(*row) for row in result]

            # Convert ComponentListFamily objects to dictionaries
            items_data = [
                {
                    'idarticle': item.idcomponent,
                    'quantity': item.quantity,
                    'name': item.name,
                    'description': item.description,
                    'image': item.image,
                    'profitmargin': item.profitmargin,
                    'barcode': item.barcode,
                    'reference': item.reference,
                }
                for item in items
            ]
            print(items_data)

            data = {'items': items_data}
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
        print(data)
        print(header)
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
        cursor.execute("select * from fn_orderssuplier_get(%s);", [id[0]])
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
        serialNumbers = json.loads(request.POST.get('serialNumbers'))
        obs = request.POST.get('obs')

        cursor.execute("select fn_generate_ordersSupplier_invoice(%s,%s,%s,%s,%s,%s);",
                       [payment_type, related_document_id, obs, invoice_type, invoice_number, invoice_date])
        doc = cursor.fetchone()
        print(doc)
        for line in documentLines:
            cursor.execute("call sp_linesInvoice_create (%s,%s,%s,%s);", [doc[0], line[0], line[6], line[4]])
            for x in serialNumbers:
                for key, value in x.items():
                    if key == line[0]:
                        for sn in value:
                            print("serial " + sn)
                            cursor.execute("CALL sp_serialGive(%s,%s)", [key, sn])
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
            equipment_id = request.POST.get('equipment_id')

            cursor.execute("SELECT fn_productionitems_delete(CAST(%s AS INTEGER));", [equipment_id])
            nice = cursor.fetchone()
            if nice[0]:
                for item in data:
                    with connections['admin'].cursor() as cursor:
                        cursor.execute("CALL sp_productionitems_add(%s,%s,%s)",
                                    [equipment_id,
                                        item['componentId'],
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

        cursor.execute("select * from view_families_list")
        result = cursor.fetchall()
        families = [Family(*row) for row in result]

        context = {'category': category, 'families': families}

        if request.method == 'POST':
            equipment_data = request.POST.get('equipment')
            print("CHEGUEI CRLH TOU AKI AAAAAAAAAAAAA", equipment_data)

            # Convert the JSON string to a Python list containing a dictionary
            equipment_list = json.loads(equipment_data)

            # Ensure the list is not empty and extract the dictionary
            if equipment_list and isinstance(equipment_list, list):
                equipment_dict = equipment_list[0]
                # Extract values from the dictionary
                name = equipment_dict.get('name', '')
                idcategory = equipment_dict.get('idcategory', '')
                description = equipment_dict.get('description', '')
                image = ""
                profit_margin = 0
                barcode = equipment_dict.get('barcode', '')
                reference = equipment_dict.get('reference', '')
                idfamily = None

                # Components
                components_data = request.POST.get('components')
                components = json.loads(components_data)

                try:
                    # Call the stored procedure using the CALL statement
                    cursor.execute("SELECT fn_articletypes_create(%s, %s, %s, %s, %s, %s, %s, %s)",
                                   [idfamily, idcategory, name, description, image, profit_margin, barcode, reference])
                    idequipment = cursor.fetchone()[0]

                    if idequipment:
                        # Process Components and call Components create
                        for component in components:
                            component_id = component['component']
                            quantity = component['quantity']

                            # Call the stored procedure for components (Modify this according to your stored procedure)
                            cursor.execute("CALL sp_productionitems_add(%s, %s, %s)",
                                           [idequipment, component_id, quantity])

                        # Commit the transaction explicitly
                        connections['admin'].commit()

                        return JsonResponse({'status': 'success'})

                except Exception as e:
                    print(f"Error executing query: {e}")

                finally:
                    cursor.close()

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
@csrf_exempt
def componentCreateViaJSON(request):
    if request.method == 'POST':
        json_file = request.FILES.get('json_file')
        if json_file:
            try:
                json_data = json_file.read().decode('utf-8')
                parsed_data = json.loads(json_data)
                insert_counter = 0
                for component in parsed_data:
                    insert_counter += 1
                    with connections['admin'].cursor() as cursor:
                        cursor.execute("CALL sp_articletypes_create(%s, %s, %s, %s, %s, %s, %s, %s)",
                                       [component['idfamily'], component['idcategory'], component['name'],
                                        component['description'], component['image'], component['profit_margin'],
                                        component['barcode'], component['reference']])
                return JsonResponse({'message': 'Foram importados ' + str(insert_counter) + ' componentes novos'})
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON file. Please upload a valid JSON file.'}, status=400)


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

        cursor.execute("select * from view_labors_list")
        result = cursor.fetchall()
        labor = [Labor(*row) for row in result]

    if request.method == 'POST':
        idlabor = request.POST.get('idlabor')

        # Call the stored procedure to update the client
        with connections['admin'].cursor() as cursor:
            cursor.execute("CALL sp_user_setLabor(%s, %s)",
                           [user_id, idlabor])
            # Commit the changes to the database

        # Redirect to the client list page after update
        return redirect('userList')

    return render(request, 'userEdit.html', {'user_id': user_id, 'labor': labor,
                                             'user': {'labor': user[4]}})


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
def productionTaskCreate(request,idproduction):
    with connections['admin'].cursor() as cursor:
        cursor.execute("SELECT * FROM fn_productions_getLines (%s);", [idproduction])
        tarefas = cursor.fetchall()

        cursor.execute("SELECT * FROM fn_production_getHeader (%s);", [idproduction])
        header = cursor.fetchall()

        cursor.execute("select * from view_warehouses_list")
        result = cursor.fetchall()
        warehouses = [Warehouse(*row) for row in result]


        return render(request, 'productionTaskCreate.html', {'tarefas': tarefas, 'header': header, 'warehouses': warehouses})

@login_required
@csrf_exempt
def productionTaskCreateSend(request):
    # Fetch the family information from the database
    with connections['admin'].cursor() as cursor:
        warehouse = request.POST.get('warehouse')
        cost = request.POST.get('cost')
        hour = request.POST.get('hour')
        quantity = request.POST.get('quantity')
        idproduction = request.POST.get('idproduction')
        idarticletype = request.POST.get('idarticletype')
        serialNumbers = json.loads(request.POST.get('serialNumbers'))
        print("Serial Numbers:", serialNumbers)

        cursor.execute("select fn_assembleequipment(%s,%s,%s,%s,%s,%s);",
            [warehouse, cost, quantity, idarticletype, idproduction, hour])
        doc = cursor.fetchall()
        print(doc)

        for x in serialNumbers:
                for key, value in x.items():
                    if key == doc[0]:
                        for sn in value:
                            print("serial " + sn)
                            cursor.execute("CALL sp_serialGive(%s,%s)", [key, sn])
        return JsonResponse({'list': idproduction})


@login_required
def productionTaskList(request):
    with connections['admin'].cursor() as cursor:
        # Call the stored procedure using the CALL statement
        cursor.execute("select  * from view_productions_list", [])
        # If the stored procedure returns results, you can fetch them
        tarefas = cursor.fetchall()

        return render(request, 'productionTaskList.html', {'tarefas': tarefas})


@login_required
def productionOrderCreate(request):
    current_user = request.user.id
    print("Current User ID:", current_user)
    with connections['admin'].cursor() as cursor:
        cursor.execute("select * from view_equipments_production")
        production = cursor.fetchall()

        cursor.execute("SELECT * FROM view_technicians", [])
        result = cursor.fetchall()
        technicians = [Tecnician(*row) for row in result]

        if request.method == 'POST':
            tecnico = request.POST.get('client')
            rows_data = json.loads(request.POST.get('rows'))
            for row in rows_data:
                print("Quantity:", row['quantity'])
                cursor.execute("CALL sp_production_create(%s,%s,%s,%s)",
                               [current_user, tecnico, row['id'], row['quantity']])
            return JsonResponse({'status': 'success'})

        context = {'production': production, 'technicians': technicians}
        return render(request, 'productionOrderCreate.html', context)


@login_required
@csrf_exempt
def getNIF(request):
    if request.method == 'POST':
        import http.client
        nif = request.POST.get('nif')
        conn = http.client.HTTPSConnection("www.nif.pt")
        payload = ''
        headers = {}
        conn.request("GET", "/?json=1&q=" + nif + "&key=" + settings.NIF_PT_TOKEN + "", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return JsonResponse({'response': data.decode("utf-8")})


@login_required
@csrf_exempt
def sendMail(request):
    from django.core.mail import send_mail
    if request.method == 'POST':
        email = request.POST.get('email')
        body_html = request.POST.get('body_html')
        send_mail(
            "Nova Fatura",
            "Aqui tem a sua dolorosa ... pague rápida por favor",

            "bytebridgessite@gmail.com",
            [email],
            fail_silently=False,
            html_message=body_html
        )
        return JsonResponse({'response': "sent"})


def register_computer_mongo(request):
    if request.method == 'POST':
        mongo_instance = pymongo.MongoClient(settings.MONGO_DB_HOST,
                                             username=settings.MONGO_USERNAME,
                                             password=settings.MONGO_PASSWORD)[settings.MONGO_DB_NAME]
        bd = mongo_instance
        collection = bd["produtos"]

        # computer_specs = json.loads(request.POST.get('computer_specs'))
        # computer_specs = Null
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        product_id = request.POST.get('product_id')

        query = {"_reference": product_id}
        update_operation = {'$push': {'properties': {field_name: field_value}}}
        result = collection.find_one(query)
        print(result)
        if result is not None:
            result = collection.update_one(query, update_operation)
        else:
            doc = {"_reference": product_id, "properties": [{field_name: field_value}]}
            collection.insert_one(doc)
        # if computer_specs == null:
        #     doc = {field_name: field_value}
        #     col.insert_one(doc)
        # else:
        #     for field,value in computer_specs:
        #         doc = {field: value}
        #         col.insert_one(doc)
        return JsonResponse({'response': "done"})

    return render(request, 'equipmentSpecs.html')
