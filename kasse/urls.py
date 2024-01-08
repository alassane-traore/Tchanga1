from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .import views

urlpatterns = [
    path('transition/',views.transit1,name='transit1'),
    path('sectors/',views.new_sector,name='sectors'),
    path('markets/',views.markets,name='market'),
    path('counter/',views.count,name='counter'),
    path('add_list/',views.add_list,name='addlist'),
    path('shopping/',views.shopping_list,name='list'),
    path('hist/',views.hist,name='history'),
    path('shop/',views.basket,name='shop'),
     path('del/<int:id>',views.removit,name="delete")
    
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)