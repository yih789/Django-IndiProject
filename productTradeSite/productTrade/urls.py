from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('Home/', views.contentList, name='contentList'),
    path('IndicontentList/', views.indicontentList, name='indicontentList'),
    path('IndicontentList/createContent/', views.create_content, name='create_content'),
    path('IndicontentList/content/<int:contentid>/', views.show_content, name='show_content'),
    path('Home/content/<int:contentid>/', views.show_Nologin_content, name='show_Nologin_content'),
    path('IndicontentList/content/<int:contentid>/update_comment/<int:commentid>/', views.update_comment, name='update_comment'),
    path('IndicontentList/content/<int:contentid>/delete_comment/<int:commentid>/', views.delete_comment, name='delete_comment'),
    path('IndicontentList/content/<int:contentid>/update_content/', views.update_content, name='update_content'),
    path('IndicontentList/content/<int:contentid>/delete_content/', views.delete_content, name='delete_content'),
    path('Home/Login/Register/', views.register, name='register'),
    path('Home/Login/', views.login, name='login'),
    path('Logout/', views.logout, name='logout'),
    path('IndicontentList/Mypage/', views.mypage, name='mypage'),
    path('IndicontentList/Mypage/update_user/', views.update_user, name='update_user'),
    path('IndicontentList/Mypage/delete_user/', views.delete_user, name='delete_user'),
    path('IndicontentList/Mypage/update_user/update_pw/', views.update_pw, name='update_pw'),
    path('usertest/', views.usertest, name='usertest'),
]

