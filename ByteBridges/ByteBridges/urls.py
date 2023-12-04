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
    
    #Clients
    path("clientsList", views.clientsList, name="clientsList"),
    path("clientsCreate", views.clientsCreate, name="clientsCreate"),
    
    #suppliers
    path("suppliersList", views.suppliersList, name="suppliersList"),
    path("suppliersCreate", views.suppliersCreate, name="suppliersCreate"),
    
    #order
    path("createOrder", views.createOrder, name="createOrder"),
    path("orderList", views.orderList, name="orderList"),
    
    #Family
    path("familyCreate", views.familyCreate, name="familyCreate"),
    
    #Equipment
    path("createEquipment", views.createEquipment, name="createEquipment"),
    
    #Component

    path("componentCreate", views.componentCreate, name="componentCreate"),

    
    
]
