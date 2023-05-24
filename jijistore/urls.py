from django.urls import path
from jijistore import views
from jijiapp.views import edit_item

app_name = 'jijistore'

urlpatterns = [
    path('storelist/', views.storelist, name='storelist' ),
    path('all_store/', views.all_store, name='all_store' ),
    path('enter_store/<str:store>/', views.enter_store, name='enter_store'),
    path('edit_store/<int:store_id>/', views.edit_store, name='edit_store'),
    # path('edit_item/<int:items_id>/', edit_item, name='edit_item'),
]