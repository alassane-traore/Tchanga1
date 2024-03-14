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
    path('updates/',views.update_sector,name='updatesec'),
    path('shop/',views.basket,name='shop'),
    path('del/<str:id>',views.removit,name="delete"),
    path('updatebusket/',views.update_busket,name='updateb'),
    path('deletebusket/',views.delete_busket,name='deleteb'),
    path('transfer/',views.transfer,name='transfer')
    
    
    
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)