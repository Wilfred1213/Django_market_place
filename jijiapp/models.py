from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.

class Category(models.Model):
    food ='Food'
    agriculture = 'Agriculture'
    computer ='Computer'
    electronics ='Electronics'
    fashion ='Fashion'
    school = 'School'
    tailor ='Tailor'
    tool ='Tools'
    phon = 'Phone'
    kitchen = 'Kitchen'
    ride = 'Ride'
    cars ='Car'
    office = 'Office'
    jowery = 'Joweries'
    
    
    
    
    CATEGORY_CHOICES=(
    (agriculture, 'Agriculture'),
    (computer, 'Computers'),
    (electronics, 'Electronics'),
    (fashion, 'Fashion'),
    (school, 'School'),
    (tailor, 'Tailor'),
    (tool, 'Tools'),
    (phon, 'Phone'),
    (kitchen, 'Kitechen'),
    (ride, 'Ride'),
    (cars, 'Cars'),
    (office, 'Office'),
    (food, 'Food'),
    (jowery, 'Joweries'),
    
    
    )
    name =models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    def __str__(self):
        return '%s' %(self.name)

class Store(models.Model):
    name = models.SlugField(unique =True, max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    discription=models.CharField(max_length=5000, null=True, blank=True)
    location =models.CharField(max_length=5000, null=True, blank=True)
    logo =models.ImageField(upload_to='logos/', default = '')
    category = models.ManyToManyField(Category, related_name ='cat')
    
    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'Store'
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length=300, null=True, blank =True)
    post_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    item=models.ForeignKey('Items', on_delete = models.CASCADE, null=True, blank = True)   

class UserItemView(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    item=models.ForeignKey('Items', on_delete = models.CASCADE, null=True, blank = True)
    
    def __str__(self):
        return self.item.title 
    class Meta:
        ordering = ['-view_date',] 
        
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    item=models.ForeignKey('Items', on_delete = models.CASCADE, null=True, blank = True)
    
class Contact(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=50, null=False)
    message = models.CharField(max_length=100, null=False)
    contact_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering =['-contact_date',]
        
class Rating(models.Model):
    item = models.ForeignKey('Items', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Items(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='supplier')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length=10, null=True, blank =True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    location =models.CharField(max_length=20, null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    thumbnails =models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name ='category')
    # comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank = True)
    

    def __str__(self):
        return self.title

    class Meta:
        ordering =['-post_date',]
        verbose_name_plural ='Items'

class Images(models.Model):
    image =models.ImageField(upload_to='media/', null=True, blank=True)
    item=models.ForeignKey(Items, on_delete = models.CASCADE, null=True, blank = True)
   

    def __str__(self):
        return str(self.item.title)
    
    class Meta:
        verbose_name_plural ='Images'
    
class Conversation(models.Model):
    item = models.ForeignKey(Items, related_name='conversations', on_delete=models.CASCADE, null = True, blank = True)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.item.title

    class Meta:
        ordering = ('-created_at',)
    
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, null = True, blank = True)
    content = models.TextField(max_length =1000, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE, null = True, blank = True)
    is_admin_reply =models.BooleanField(default = False)
     
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ('-created_at',)
class ConversationCount(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages_count', on_delete=models.CASCADE, null = True, blank = True)   
    message_count = models.IntegerField(default=1)

# counting inbox
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=ConversationMessage)
@receiver(post_delete, sender=ConversationMessage)
def update_conversation_message_count(sender, instance, **kwargs):
    try:
        conversation = getattr(instance, 'conversation', None)
        
        if conversation is None:
            return  # Skip further processing if the conversation is not available
        
        conversation_count, created = ConversationCount.objects.get_or_create(conversation=conversation)
        conversation_count.message_count = conversation.messages.count()
        conversation_count.save()
    except ObjectDoesNotExist:
        pass


    
class Suppliers(models.Model):
    items = models.OneToOneField(Items, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        
        verbose_name_plural = 'Supplier'

class Counts(models.Model):
    image = models.ForeignKey(Images, on_delete = models.CASCADE, null=True, blank = True)
class HomeImage(models.Model):
    image = models.ImageField(upload_to = 'HomeImage')

# signal
@receiver(post_save, sender=ConversationMessage)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        if conversation and conversation.item:
            item_store = conversation.item
            user = instance.created_by

            # send email to supplier if message was created by customer
            if user != item_store.user:
                supplier_email = item_store.user.email
                subject = f'New message about {item_store.title}'
                message = f'You have a new message about {item_store.title} from {instance.created_by}.\n\n'
                message += f'Message Content: {instance.content}\n\n'
                message += f'Conversation: {instance.conversation}'
                from_email = 'mathiaswilfred7@yahoo.com'
                recipient_list = [supplier_email]
                send_mail(subject, message, from_email, recipient_list)

            # send email to customer if message was created by supplier
            elif user == item_store.user:
                for member in conversation.members.all():
                    if member != user:
                        customer_email = member.email
                        subject = f'New reply about {item_store.title}'
                        message = f'{item_store.user.username} replied to your message at Wilf Marke Place about {item_store.title}.\n\n'
                        message += f'Message Content: {instance.content}\n\n'
                        message += f'Conversation: {instance.conversation}'
                        from_email = 'mathiaswilfred7@yahoo.com'
                        recipient_list = [customer_email]
                        send_mail(subject, message, from_email, recipient_list)
