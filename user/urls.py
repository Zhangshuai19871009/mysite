from django.urls import path
from . import views

urlpatterns = [
    # 弹框式登录
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    # 登录
    path('login/', views.login, name='login'),
    # 注册
    path('register/', views.register, name='register'),
    # 退出登录
    path('logout/', views.logout, name='logout'),
    # 用户信息
    path('user_info/', views.user_info, name='user_info'),
    # 修改昵称
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    # 绑定邮箱
    path('bind_email/', views.bind_email, name='bind_email'),
    # 发送验证码
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    # 修改密码
    path('change_password/', views.change_password, name='change_password'),
    # 忘记密码
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]