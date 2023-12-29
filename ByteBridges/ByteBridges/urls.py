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

urlpatterns = [
    path("dashboard", views.IndexPage, name="dashboard"),
    #path("dashboard", views.dashboard, name="dashboard"),
    path("loginForm", views.loginForm, name="loginForm"),
    path("", views.Login, name="login"),
    path('get_articles/', views.get_articles, name='get_articles'),

    #Clients
    path("clientCreate", views.clientCreate, name="clientCreate"),
    path("clientList", views.clientList, name="clientList"),
    path('clientEdit/<int:client_id>/', views.clientEdit, name='clientEdit'),
    path('clientDelete', views.clientDelete, name='clientDelete'),
    
    #suppliers
    path("supplierCreate", views.supplierCreate, name="supplierCreate"),
    path("supplierList", views.supplierList, name="supplierList"),

    path('supplierEdit/<int:idsupplier>/', views.supplierEdit, name='supplierEdit'),
    path('supplierDelete', views.supplierDelete, name='supplierDelete'),

    #order
    path("orderSupplierCreate", views.orderSupplierCreate, name="orderSupplierCreate"),
    path("orderSupplierList", views.orderSupplierList, name="orderSupplierList"),
    path("orderClientCreate", views.orderClientCreate, name="orderClientCreate"),
    path("orderClientList", views.orderClientList, name="orderClientList"),

    #documentsSupplier
    path("documentsSupplier", views.documentsSupplier, name="documentsSupplier"),
    path("documentsSupplierFetch", views.documentsSupplierFetch, name="documentsSupplierFetch"),

    
    #Family
    path("familyCreate", views.familyCreate, name="familyCreate"),
    path("familyList", views.familyList, name="familyList"),
    path('familyEdit/<int:idSupplier>/', views.familyEdit, name='familyEdit'),

    
    #Equipment
    path("equipmentCreate", views.equipmentCreate, name="equipmentCreate"),
    path("equipmentList", views.equipmentList, name="equipmentList"),
    path('equipmentEdit/<int:equipment_id>/', views.equipmentEdit, name='equipmentEdit'),
    
    #Component
    path("componentCreate", views.componentCreate, name="componentCreate"),
    path("componentList", views.componentList, name="componentList"),

    #Users
    path("userList", views.userList, name="userList"),
    path('userEdit/<int:user_id>/', views.userEdit, name='userEdit'),
    path('userDelete', views.userDelete, name='userDelete'),

    #Labor
    path("laborCreate", views.laborCreate, name="laborCreate"),
    path("laborList", views.laborList, name="laborList"),
    path('laborEdit/<int:labor_id>/', views.laborEdit, name='laborEdit'),
    path('laborDelete', views.laborDelete, name='laborDelete'),

]
