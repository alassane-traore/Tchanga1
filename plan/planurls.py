from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from .import views

urlpatterns = [
    path('add/',views.add,name='add'),
    path('months/',views.months,name='months'),
    path('weeks/',views.week,name='weeks'),
    path('week days/',views.days,name='days'),
    path('classes/',views.types,name='types'),
    path('lines/',views.add_week,name="lines"),
    path('transit/',views.transit,name="transit"),
    #path('bird/',views.give_tone,name="ringer"),
    path('t/',views.new_time,name="tchanger"),
    path('update/<int:id>',views.give_to_update_object,name="update"),
    path('delete/<int:id>',views.remov,name="delete")
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
