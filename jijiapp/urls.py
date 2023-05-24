
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index' ),
    path('itemupload/<int:store_id>', views.itemupload, name='itemupload' ),
    # path('chat/<int:item_id>/', views.chat, name='chat' ),
    path('detail/<str:pk>/', views.detail, name='detail' ),
    path('chatdetail/<int:pk>/', views.chatdetail, name='chatdetail' ),
    path('inbox/', views.inbox, name='inbox' ),
    
    path('signup/', views.signup, name='signup' ),
    path('signout/', views.signout, name='signout' ),
    
    path('deletstore/<int:store_id>/', views.deletstore, name='deletstore' ),
    path('deleteitem/<int:item_id>/', views.deleteitem, name='deleteitem' ),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_inbox/<int:item_id>/', views.delete_inbox, name='delete_inbox' ),
    path('delete_con/<int:item_id>/', views.delete_con, name='delete_con' ),
    
    path('favorite/', views.favorite, name='favorite'),
    path('delete_fav/<int:item_id>/', views.delete_fav, name='delete_fav' ),
    path('contact/', views.contact, name='contact' ),
    # path('home/inbox/get_new_messages/', views.get_new_messages, name='get_new_messages'),
    path('reset_message_count/', views.reset_message_count, name='reset_message_count'),
    

]