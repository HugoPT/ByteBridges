"""
URL configuration for ByteBridges project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ByteBridges import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard", views.IndexPage, name="dashboard"),
    path("tecMainPage", views.IndexPage, name="tecMainPage"),
    path("login/", auth_views.LoginView.as_view(template_name='Login.html'), name="login"),
    path("", views.Homepage, name="Homepage"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),


    path('get_articles/', views.get_articles, name='get_articles'),
    path('productionEquipmentCreate/get_articles/', views.get_articles, name='get_articles'),
    path('productionEquipmentEdit/get_articles/', views.get_articles, name='get_articles'),

    # Clients
    path("clientCreate", views.clientCreate, name="clientCreate"),
    path("clientList", views.clientList, name="clientList"),
    path('clientEdit/<int:client_id>/', views.clientEdit, name='clientEdit'),
    path('clientDelete', views.clientDelete, name='clientDelete'),

    # suppliers
    path("supplierCreate", views.supplierCreate, name="supplierCreate"),
    path("supplierList", views.supplierList, name="supplierList"),
    path('supplierEdit/<int:idsupplier>/', views.supplierEdit, name='supplierEdit'),
    path('supplierDelete', views.supplierDelete, name='supplierDelete'),

    # order
    path("orderSupplierCreate", views.orderSupplierCreate, name="orderSupplierCreate"),
    path("orderSupplierList", views.orderSupplierList, name="orderSupplierList"),
    path("orderClientCreate", views.orderClientCreate, name="orderClientCreate"),
    path("orderClientList", views.orderClientList, name="orderClientList"),
    path("orderSupplierLinesFetch", views.orderSupplierLinesFetch, name="orderSupplierLinesFetch"),
    path("orderClientLinesFetch", views.orderClientLinesFetch, name="orderClientLinesFetch"),
    path('orderClientFetchInvoice/<int:idorder>/', views.orderClientFetchInvoice, name='orderClientFetchInvoice'),
    path('orderSupplierExportJson', views.orderSupplierExportJson, name='orderSupplierExportJson'),

    # documentsSupplier
    path("invoiceSupplierRegister", views.invoiceSupplierRegister, name="invoiceSupplierRegister"),
    path("documentsSupplierFetch", views.documentsSupplierFetch, name="documentsSupplierFetch"),
    path("documentsSupplierLinesFetch", views.documentsSupplierLinesFetch, name="documentsSupplierLinesFetch"),
    path("documentsSupplierRegisterInvoice", views.documentsSupplierRegisterInvoice,name="documentsSupplierRegisterInvoice"),
    # path("documentsSupplierRegisterInvoiceHeader", views.documentsSupplierRegisterInvoiceHeader, name="documentsSupplierRegisterInvoiceHeader"),
    # path("documentsSupplierRegisterInvoiceLines", views.documentsSupplierRegisterInvoiceLines, name="documentsSupplierRegisterInvoiceLines"),

    # Family
    path("familyCreate", views.familyCreate, name="familyCreate"),
    path("familyList", views.familyList, name="familyList"),
    path('familyEdit/<int:family_id>/', views.familyEdit, name='familyEdit'),

    # Equipment
    path("equipmentCreate", views.equipmentCreate, name="equipmentCreate"),
    path("equipmentList", views.equipmentList, name="equipmentList"),
    path('equipmentEdit/<int:equipment_id>/', views.equipmentEdit, name='equipmentEdit'),
    path('equipmentDelete', views.equipmentDelete, name='equipmentDelete'),
    path('productionEquipmentCreate/<int:equipment_id>/', views.productionEquipmentCreate, name='productionEquipmentCreate'),

    # Component
    path("componentCreate", views.componentCreate, name="componentCreate"),
    path("componentCreateViaJSON", views.componentCreateViaJSON, name="componentCreateViaJSON"),
    path("componentList", views.componentList, name="componentList"),
    path('componentEdit/<int:component_id>/', views.componentEdit, name='componentEdit'),
    path('componentDelete', views.componentDelete, name='componentDelete'),

    # Stocks
    path("stockList", views.stockList, name="stockList"),
    path("stockMovementList", views.stockMovementList, name="stockMovementList"),

    # Users
    path("userList", views.userList, name="userList"),
    path('userEdit/<int:user_id>/', views.userEdit, name='userEdit'),

    # Labor
    path("laborCreate", views.laborCreate, name="laborCreate"),
    path("laborList", views.laborList, name="laborList"),
    path('laborEdit/<int:labor_id>/', views.laborEdit, name='laborEdit'),
    path('laborDelete', views.laborDelete, name='laborDelete'),

    # Production
    path("productionOrderCreate", views.productionOrderCreate, name="productionOrderCreate"),

    # TaskList
    path("productionTaskList", views.productionTaskList, name="productionTaskList"),
    path("tecProductionTaskList", views.tecProductionTaskList, name="tecProductionTaskList"),
    path('productionTaskCreate/<int:idproduction>/', views.productionTaskCreate, name='productionTaskCreate'),
    path("productionTaskCreateSend", views.productionTaskCreateSend, name="productionTaskCreateSend"),

    # Items
    path('get_items/', views.get_items, name='get_items'),

    # Utils
    path("getNIF", views.getNIF, name="getNIF"),
    path("sendMail", views.sendMail, name="sendMail"),
    path('register_computer_mongo/<int:equipment_id>/', views.register_computer_mongo, name="register_computer_mongo"),
    path('register_computer_mongo_send', views.register_computer_mongo_send, name='register_computer_mongo_send'),
    
    path('shoppingStore', views.shoppingStore, name='shoppingStore'),


    #Reporting
    path("reporting", views.reporting, name="reporting"),
    
    
    #TEC PAGE
    path("weeklyProduction", views.weeklyProduction, name="weeklyProduction"),
    path("pendentProductions", views.pendentProductions, name="pendentProductions"),
    path("delayedProduction", views.delayedProduction, name="delayedProduction"),
    
    path("getCounts", views.getCounts, name="getCounts"),

]
