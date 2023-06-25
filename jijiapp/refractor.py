from jijiapp.models import *
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib import messages


def rate_item(request, item_id):
    item = Items.objects.get(id=item_id)
    ratings = Rating.objects.filter(item=item, user =request.user)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating == None:
            messages.info(request, 'please rate this item!')
            return redirect('detail', pk=item_id)
        messages.info(request, 'Thank you for rating this item!')
        
        if not Rating.objects.filter(item=item, user=request.user).exists():
            
            new_rating = Rating.objects.create(item=item, user=request.user, rating=rating)
            return redirect('detail', pk=item_id)
        else:
            update_r =ratings.first()
            update_r.rating =rating
            update_r.user =request.user
            update_r.item =item
            update_r.save()
            messages.info(request, 'Thank you for rating  this item!')
            return redirect('detail', pk=item_id)
        
            
            new_rating =None
def get_message_count(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    count = conversations.count()
    return count               
                

def view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST' and 'item_id' in request.POST:
            item_id = request.POST['item_id']
            item = Items.objects.get(id=item_id)
            
            # check if the current user has already viewed the item
            viewed = UserItemView.objects.filter(item=item, user=user)
            if viewed:
                view = viewed.first()
                # if the user has already viewed the item, update the view date
                # viewed.update(view_date=timezone.now())
                view.view_date = timezone.now()
                view.save()
            else:
                # if the user has not viewed the item, create a new view record
                viewed = UserItemView.objects.create(user=user, item=item)
                
            return item
    
def category(request, item_id):
   
    try:
        item = Items.objects.get(id=item_id)
        cat = item.category.all()  # Get the related categories
        categor = Items.objects.filter(category__in=cat) 
    except Items.DoesNotExist:
        cat=None
        categor = None
        messages.error(request, f'No such category yet')
    
    return categor