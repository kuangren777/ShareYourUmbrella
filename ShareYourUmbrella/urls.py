"""ShareYourUmbrella URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from UmbrellaApp import views
from UmbrellaApp import api

urlpatterns = [
    path("admin/", admin.site.urls),
    # 登陆注册
    path("login/", views.login_page),
    path("accounts/login/", views.account_login_page),

    path("logout/", views.logoutUser),
    path("register/", views.register),

    # 首页
    path("", views.test),

    # 个人界面
    path("delete/", views.user_delete),

    # 功能
    path("myinfo/", views.myinfo),
    path("user/<str:pk>/", views.user),
    path("change_password/", views.change_password),

    # 创建订单
    path("creat_order/", views.creat_order),
    path("creat_order/borrow/", views.creat_order_borrow),
    path("creat_order/back/", views.creat_order_back),

    # 入库伞
    path("import_umbrella/", views.import_umbrella),
    path("report_repair_umbrella/", views.report_repair_umbrella),
    # path('report-repair/', views.report_repair, name='report-repair'),
    path('report-repair/<int:umbrella_id>/', views.report_repair, name='report-repair'),
    path('update-repair/<int:umbrella_id>/', views.update_repair, name='update-repair'),

    # 伞调度
    path('umbrella-dispatch/<int:umbrella_id>/', views.umbrella_dispatch, name='umbrella_dispatch'),

    # path("get_pending_repairs/", views.get_pending_repairs),
    # path('get_umbrellas_for_repair/<int:repair_type_id>/', views.get_umbrellas_for_repair,
    #      name='get_umbrellas_for_repair'),

    path('get_umbrellas_for_repair/<int:repair_type_id>', views.get_umbrellas_for_repair,
         name='get_umbrellas_for_repair'),
    path('get_umbrellas_for_repair/', views.get_umbrellas_for_repair, name='get_umbrellas_for_repair'),

    path('get_repair_notes/<int:umbrella_id>', views.get_repair_notes, name='get_repair_notes'),
    path('get_repair_notes/', views.get_repair_notes, name='get_repair_notes'),

    path('add_comment/<int:diary_id>/', views.add_comment, name='add_comment'),

    path("repair_umbrella/", views.repair_umbrella),

    # 放置伞
    path("place_umbrella/", views.place_umbrella),

    # 查询伞
    path("place_detail/<str:pk>/", views.place_detail),

    # 账户充值
    path("recharge_account/", views.recharge_account),

    # 添加优惠券
    path("add_coupon/", views.add_coupon),

    # 添加站点警报
    path("add_location_alarm/", views.add_location_alarm),

    # 添加站点警报
    path("delete_location_alarm/", views.delete_location_alarm),
    path("delete_user_alarm/", views.delete_user_alarm),
    path("delete_umbrella_alarm/", views.delete_umbrella_alarm),

    # 添加用户警报
    path("add_user_alarm/", views.add_user_alarm),
    path("add_umbrella_alarm/", views.add_umbrella_alarm),

    # 后台管理界面
    path("ad/test/", views.test),
    path("ad/userinfo/", views.userinfo),

    # 随机数据
    path("random/", views.ran),

    # 找空位置
    path('get_empty_positions/<int:site_id>/', views.get_empty_positions, name='get_empty_positions'),

    path('get_free_positions/<str:site_id>/', views.get_free_positions, name='get_free_positions'),

    # 重置密码
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
         name='password_reset_complete'),

    # path('api/user/login', api.user_login, name='用户登录')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
