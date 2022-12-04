from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('edit_item/<int:item_id>/', views.EditItem.as_view(), name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('mark_item/<int:item_id>/', views.mark_item, name='mark_item'),
]