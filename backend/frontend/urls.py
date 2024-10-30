from django.urls import path
from .views import index, login_view, logout_view, get_users

urlpatterns = [
    path('', index),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/users/', get_users, name='get_users'),

]