from django.urls import path
from apps.monitor import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name="dashboard"),
]