from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('logout', views.logout_view, name='logout_view'),
    path('createTask', views.createteask, name='createTask'),
    path('completetask', views.completetask, name='completetask'),
    path('deleteatsk', views.deletetask, name='deletetask'),
    path('deletealltasks', views.deletealltasks, name='deleteaslltasks'),
    path('profile', views.profile, name='profile'),
    path('photogrid', views.photogrid, name='photogrid'),
    path('addimage', views.addimage, name='addimage'),
    path('deletephoto/<int:photoid>', views.deletephoto, name='deletephoto'),
    path('editphoto/<int:photoid>', views.editphoto, name='editphoto'),
]


