from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createMail", views.createMailPage, name="createMailPage"),
    path("sendMail", views.sendMailPage, name="sendMailPage"),
]
