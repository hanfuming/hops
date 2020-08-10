from django.urls import path
from apps.asset import views

urlpatterns = [
    path('host', views.HostView.as_view(), name="host"),
    path('cdb', views.CdbView.as_view(), name="cdb"),
    path('product', views.ProductView.as_view(), name="product"),
]