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
    path("clientCreate", views.clientCreate, name="clientCreate"),
    path("clientList", views.clientList, name="clientList"),
    path('get-nif/<str:nif>/', views.get_nif_data, name='get_nif_data'),

    #suppliers
    path("supplierCreate", views.supplierCreate, name="supplierCreate"),
    path("supplierList", views.supplierList, name="supplierList"),
    
    #order
    path("orderCreate", views.orderCreate, name="orderCreate"),
    path("orderList", views.orderList, name="orderList"),
    
    #Family
    path("familyCreate", views.familyCreate, name="familyCreate"),
    
    #Equipment
    path("equipmentCreate", views.equipmentCreate, name="equipmentCreate"),
    path("equipmentList", views.equipmentList, name="equipmentList"),
    
    #Component
    path("componentCreate", views.componentCreate, name="componentCreate"),
    path("componentList", views.componentList, name="componentList"),

]
