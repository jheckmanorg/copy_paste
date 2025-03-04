from django.urls import path
from . import views

urlpatterns = [
    path('', views.paste_list, name='paste_list'),
    path('create/', views.create_paste, name='create_paste'),
    path('extend/<int:paste_id>/', views.extend_paste, name='extend_paste'),
]
