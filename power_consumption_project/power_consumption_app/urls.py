from django.urls import path
from . import views

urlpatterns = [
    path('power/',views.power, name = 'power'),
    path('voltage/',views.voltage,name = 'voltage'),
    path('elec_con/',views.elec_con,name = 'elec_con'),
    path('',views.home,name='home'),
    path('database/',views.database,name = 'database'),
    path('query/', views.query, name='query'),
]
