from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Store(models.Model):
#     name = models.SlugField(unique =True, max_length=50)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
#     create_date = models.DateTimeField(auto_now_add=True, null=True)
#     discription=models.CharField(max_length=5000, null=True, blank=True)
#     location =models.CharField(max_length=5000, null=True, blank=True)
#     logo =models.ImageField(upload_to='logos/', default = '')
#     def __str__(self):
#         return '%s' % (self.name)
    
#     class Meta:
#         ordering = ['-name']
#         verbose_name_plural = 'Store'
    
class Items(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='store/')
    # store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False)
    date_uploaded=models.DateTimeField(auto_now_add=True)
    price =models.DateTimeField(auto_now_add=True)
    discription=models.CharField(max_length=5000, null=True, blank=True)
    
    def __str__(self):
        return '%s' % (self.title)
    
    class Meta:
        ordering = ['-title']
        verbose_name_plural = 'Items'
    
