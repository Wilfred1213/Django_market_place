from django.contrib import admin
from .models import *

# Register your models here.
class imagesAdmin(admin.StackedInline):
    model = Images
    
    extra =1

@admin.register(Items)
class displayAdmin(admin.ModelAdmin):
    list_display =['title', 'description', 'price', 'phone', 'location','post_date']
    inlines =[imagesAdmin]

    class Meta:
        model = Items
        

@admin.register(Images)
class displayAdmin(admin.ModelAdmin):
    list_display =['image','item']
    
@admin.register(ConversationMessage)
class displayAdmin(admin.ModelAdmin):
    list_display =['content', 'created_at', 'created_by']
    
@admin.register(Conversation)
class displayAdmin(admin.ModelAdmin):
    list_display =['item', 'created_at']
    
    
admin.site.register(Store)
admin.site.register(Suppliers)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserItemView)
admin.site.register(Favorite)
admin.site.register(Contact)
admin.site.register(Rating)
admin.site.register(HomeImage)
admin.site.register(ConversationCount)


