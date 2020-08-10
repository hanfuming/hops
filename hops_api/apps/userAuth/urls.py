from django.urls import path
from apps.userAuth import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('getInfo', views.UserInfoView.as_view(), name="getInfo"),
    path('getRouters', views.RoutesView.as_view(), name="getRouters"),
    path('user', views.UserManageView.as_view(), name="user"),
    path('role', views.roleManageView.as_view(), name="role"),
    path('menu', views.roleMenusView.as_view(), name="menu"),
    path('menu/treeselect/', views.menuTreeView.as_view(), name="menuTree"),

]