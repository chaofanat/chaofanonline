from django.contrib import admin
from django.urls import path, include
from metaphysics import views

urlpatterns = [
   path("", views.index, name="metaphysicsindex")
]