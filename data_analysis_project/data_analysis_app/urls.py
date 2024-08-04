from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('visualize/', views.visualize_data, name='visualize_data'),
    path('data/', views.view_data, name='view_data'),
]
