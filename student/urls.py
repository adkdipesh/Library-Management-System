from django.urls import path
from . import views

urlpatterns = [
    path('', views.slogin, name='slogin-page'),
    path('login/', views.slogin), 
    
    path('logout/', views.slogout, name='slogout-page'),
    
    path('index/', views.home, name='shome-page'),
    path('borrow_book/', views.borrowbook , name='bb-page'),
    path('return_book/', views.returnbook , name='rb-page'),    
]