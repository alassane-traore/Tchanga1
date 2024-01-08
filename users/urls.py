from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.signup,name="signup" ),
    path('profile/',views.profile,name="profile" ),
    path('editprofile/',views.edit_profile,name="profiledit" ),
    path('login/',views.loginin,name="login" ),
    path('logout/',views.logingout,name="logout"),
    path('home/',views.home,name="home"),
    path('',views.welcome,name="wlc")

]
