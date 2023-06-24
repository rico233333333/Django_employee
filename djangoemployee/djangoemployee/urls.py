"""djangoemployee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from app01 import views,admin_,account
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),


    path('depart_list/',views.depart_list),
    path('depart_add/',views.depart_add),
    path('depart_del/',views.depart_del),
    path('depart_edit/<int:nid>',views.depart_edit),
    path('index/',views.index),
    path('user_list/',views.user_list),
    path('user_add/',views.user_add),
    path('user_add_modelform/',views.user_add_modelform),
    path('user_del/',views.user_del),
    path('user_edit/<int:nid>',views.user_edit),
    path('pretynum_list/',views.pretynum_list),
    path('pretynum_add/',views.pretynum_add),
    path('pretynum_edit/<int:nid>',views.pretynum_edit),
    path('pretynum_del/',views.pretynum_del),

    # 管理员用户管理
    path("admin_list/",admin_.admin_list),
    path("admin_add/",admin_.admin_add),
    path("admin_edit/<int:nid>",admin_.admin_edit),
    path("admin_del/<int:nid>",admin_.admin_del),
    path("admin_reset/<int:nid>",admin_.admin_reset),

    # 用户登录模块
    path("login/",account.login),
    path("loginout/",account.loginout),

]
