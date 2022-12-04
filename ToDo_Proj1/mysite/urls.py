from django.urls import path
from . import views

app_name = 'mysite'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('resume/', views.Resume.as_view(), name='resume'),
]