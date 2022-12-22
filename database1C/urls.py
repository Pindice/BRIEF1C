from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.produits, name="ImportProduits"),
    path('', views.facture, name="ImportFacture"),
    path('', views.compose, name="ImportCompose")
]