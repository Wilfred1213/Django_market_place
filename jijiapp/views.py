from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Count, Q
from jijistore.views import enter_store
from django.contrib.auth import logout
from django.urls import reverse
from django.views.generic import ListView
from django.utils import timezone
from jijiapp.refractor import view, rate_item, get_message_count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET

from time import sleep


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'jijiapp/registration/signup.html', {
        'form': form
    })
    
def signout(request):
    logout(request)
    messages.info(request, 'You just logged out, login again!')
    return redirect('login')
# end of uth
@login_required
def contact(request):
    contacts =Contact.objects.all()
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        contact_info = Contact.objects.create(name = name, email=email, message= message)
        messages.info(request, f'thank you {name} for contacting us. We will get back to you soon!')
        return redirect('contact')
    context = {
        'contacts':contacts,
    }
    return render(request, 'jijiapp/contact.html', context)
@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user)

    count = 0
    for conversation in conversations:
        try:
            conversation_count = ConversationCount.objects.get(conversation=conversation)
            count += conversation_count.message_count
        except ConversationCount.DoesNotExist:
            pass
    
    if request.method == 'POST' and 'reset_message_count' in request.POST:
        ConversationCount.objects.filter(conversation__members=request.user).update(message_count=0)
        return redirect('inbox')
    
    context = {
        'conversations': conversations,
        'count': count,
    }
    
    return render(request, 'jijiapp/inbox.html', context)

def reset_message_count(request):
    if request.method == 'POST':
        ConversationCount.objects.filter(conversation__members=request.user).update(message_count=0)
        return redirect('inbox')
@login_required  
def index(request):
    
    img = HomeImage.objects.all()
    homeimage = img.first()
    user = request.user
    
    conversations = Conversation.objects.filter(members=request.user)

    # count = 0
    # for conversation in conversations:
    #     recent_message = conversation.messages.order_by('-created_at').first()
    #     if recent_message:
    #         count += 1
    count = 0
    for conversation in conversations:
        try:
            conversation_count = ConversationCount.objects.get(conversation=conversation)
            count += conversation_count.message_count
        except ConversationCount.DoesNotExist:
            pass
    

    if request.method == 'POST' and 'reset_message_count' in request.POST:
        ConversationCount.objects.filter(conversation__members=request.user).update(message_count=0)
        return redirect('inbox')
    
    
    if user.is_authenticated:
         
            # hiding favorite when user added
        if request.method == 'POST' and 'favorite' in request.POST:
            favorite_id = request.POST.get('favorite_id')
            favorite_item = Items.objects.get(id=favorite_id)
            Favorite.objects.create(user=request.user, item=favorite_item)
        
        # Get favorite items
        fav = Items.objects.filter(favorite__user=user)
        # end
        item = Items.objects.all()
    
        # search logic
        name = request.GET.get('search')
        
        item_category = item.filter(Q(category__name__icontains=name) 
                                | Q(description__icontains=name) 
                                | Q(title__icontains=name) 
                                | Q(title__istartswith=name) 
                                | Q(category__name__istartswith=name)) if name else None
        
        
            # return JsonResponse({'count': count})
        viewed_items = Items.objects.filter(useritemview__user=user).order_by('-useritemview__view_date')[:3]
    else:
        
        item = Items.objects.all()
        
        # search logic
        name = request.GET.get('search')
        
        item_category = item.filter(Q(category__name__icontains=name) 
                                | Q(description__icontains=name) 
                                | Q(title__icontains=name) 
                                | Q(title__istartswith=name) 
                                | Q(category__name__istartswith=name))if name else None#if name else messages.info(request, 'no item with name %s' %(name))
        # if name ==None:
        #     messages.info(request, 'Dont leave blank')
            
    
    
        viewed_items = None
        
        fav =None
    
    context = {
        'user': user,
        'all_item': item,
        'count': count,
        'name': name,
        'viewed_items': viewed_items,
        'item_category': item_category,
        'homeimage':homeimage,
        'favs': fav,
    }
    
    item = view(request)
    if item:
        return redirect('detail', pk=item.id)
   
    return render(request, 'jijiapp/index.html', context)


@login_required
def detail(request, pk):
    img = HomeImage.objects.all()
    homeimage = img.first()
    user = request.user
    item =Items.objects.all()
    # item_url = reverse('chat', args=[pk])
    chat_url = reverse('chatdetail', args=[pk])
    
    try:
        items = Items.objects.get(pk = pk)
     
    except Items.DoesNotExist:
        items = Items.objects.filter(title = pk)
    store_url = items.store.id
    store_routing = reverse('jijistore:enter_store', args = [store_url])
    
    # counts = Images.objects.aggregate(count = Count('image'))
    conversations = Conversation.objects.filter(members=request.user)

    # count = 0
    # for conversation in conversations:
    #     recent_message = conversation.messages.order_by('-created_at').first()
    #     if recent_message:
    #         count += 1
    count = 0
    for conversation in conversations:
        try:
            conversation_count = ConversationCount.objects.get(conversation=conversation)
            count += conversation_count.message_count
        except ConversationCount.DoesNotExist:
            pass
    

    if request.method == 'POST' and 'reset_message_count' in request.POST:
        ConversationCount.objects.filter(conversation__members=request.user).update(message_count=0)
        return redirect('inbox')
    
    
    if user.is_authenticated:
         
            # hiding favorite when user added
        if request.method == 'POST' and 'favorite' in request.POST:
            favorite_id = request.POST.get('favorite_id')
            favorite_item = Items.objects.get(id=favorite_id)
            Favorite.objects.create(user=request.user, item=favorite_item)
    
    # feedback section
    comments = Comment.objects.filter(item=items)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            detail = form.cleaned_data['detail']
            comment = Comment.objects.create(content = detail, user=user, item=items )
            
            return JsonResponse({'detail': comment.content, 
                                 'user': comment.user.username, 'post_date': comment.post_date.strftime("%Y-%m-%d %H:%M:%S")})
            # # messages.info(request, 'Thank you for the feed back')
            # return redirect('detail', pk=pk)
    else:
        form = CommentForm()
        
    # search section
   
    name = request.GET.get('search')
    item_category = item.filter(Q(category__name__icontains=name) 
                            | Q(description__icontains=name) 
                            | Q(title__icontains=name) 
                            | Q(title__istartswith=name) 
                            | Q(category__name__istartswith=name))if name else None
    
    viewed_items = Items.objects.filter(useritemview__user=user).order_by('-useritemview__view_date')[:3]
    
    # rating
    rate_item(request, pk)
    
    context = {
        # 'rating':rating,
        'detail_item':items,
        'comments': comments,
        'form': form,
        'all_item':item,
        'user':user,
        'count':count,
        # 'item_url':item_url,
        'chat_url':chat_url,
        'store_routing':store_routing,
        'name':name,
        'item_category':item_category,
        'viewed_items':viewed_items,
        'homeimage':homeimage,
    }
    
    item = view(request)
    if item:
        return redirect('detail', pk=item.id)
    return render(request, 'jijiapp/jijidetail.html', context)


@login_required
def itemupload(request, store_id):
    user = request.user
    items = Items.objects.filter(user=request.user)[:4]
    item_url = reverse('itemupload', args=[store_id])
    i = Items.objects.filter(user=request.user)
    categories = Category.objects.filter(name__in=i.values('category'))
    
    if store_id:
        store = get_object_or_404(Store, pk=store_id)
    else:
        store = None

    if request.method == 'POST':
        itemsform = ItemsForm(request.POST, request.FILES)
        imageforms = ImageForm(request.POST, request.FILES)

        file = request.FILES.getlist('image')

        if all([itemsform.is_valid(), imageforms.is_valid()]):
            item = itemsform.save(commit=False)
            item.user = request.user
            item.store = store
            item.save()
            
            selected_category_id =itemsform.cleaned_data['category']
            selected_categories=Category.objects.filter(id__in = selected_category_id)
            item.category.set(selected_categories)
            

            for i in file:
                Images.objects.create(item=item, image=i)

            return redirect('index')

        return redirect('itemupload')

    imageforms = ImageForm()
    itemsform = ItemsForm()
    context = {
        'imageforms': imageforms,
        'itemsform': itemsform,
        'items': items,
        'store': store,
        'item_url': item_url
    }
    return render(request, 'jijiapp/itemform.html', context)


        
# this is the section for chat between user and supplier


            
@login_required   
def delete_inbox(request, item_id):
    conversations = get_object_or_404(Conversation, id=item_id)
    # conversations = Conversation.objects.filter(item=item)
    
    conversations.delete()
    
    return redirect('inbox')

@login_required   
def delete_con(request, item_id):
    user = request.user
    try:
        conversation = Conversation.objects.get(id=item_id)
    except Conversation.DoesNotExist:
        raise Http404("Conversation does not exist")
    
    if user == conversation.item.user:
        conversation.delete()
        messages.success(request, 'Conversation deleted successfully')
    else:
        messages.error(request, 'You are not authorized to delete this conversation')

    return redirect('inbox')

@login_required
def chatdetail(request, pk):
    
    item = get_object_or_404(Items, pk=pk)
    
    conversation = Conversation.objects.filter(item=item, members__in=[request.user.id])
    
    if conversation.exists():
        conversation=conversation.first()
    else:
        conversation = Conversation.objects.create(item=item)
        conversation.members.add(request.user)
        conversation.members.add(item.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # if conversation is not None:
            conversation.save()
                # print(str(Conversation.objects.filter(item=item, members__in=[request.user.id]).first().query))

            return redirect('chatdetail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'jijiapp/chatdetail.html', {'conversation': conversation,'form': form, 'item':item})


@login_required
def deletstore(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    delete_url = reverse('deletstore', args=[store_id])
    item = Items.objects.filter(store = store)
     
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            if store.author == request.user:
                store.delete()
                item.delete()
                messages.success(request, 'Store deleted successfully')
                return redirect('jijistore:all_store')
            else:
                messages.error(request, 'You cannot delete this store')
                return redirect('jijistore:all_store')
        else:
            return redirect('jijistore:all_store')
    else:
        return render(request, 'jijiapp/confirm_delete.html', {'store': store, 'delete_url': delete_url})
    
    
# deleting items
@login_required
def deleteitem(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    delete_url = reverse('deleteitem', args=[item_id])
    # item = Items.objects.filter(store = store)
     
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            if item.user == request.user:
                item.delete()
                
                messages.success(request, f'{item.title} deleted successfully')
                return redirect('jijistore:all_store')
            else:
                messages.error(request, 'You cannot delete this store')
                return redirect('index')
        else:
            return redirect('index')
    else:
        return render(request, 'jijiapp/confirm_delete_item.html', {'item': item, 'delete_url': delete_url})


# editing item
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    # images = Images.objects.filter(item=item).first()
    images = item.images_set.all()
    store_id = Store.objects.first().id #this is here for url routing
    store = get_object_or_404(Store, author=request.user.id)
    item_edit_url = reverse('edit_item', args=[item_id])
    
    if request.method == 'POST':
        itemsforms =ItemsForm(request.POST, request.FILES, instance=item)
        imageforms = ImageForm(request.POST, request.FILES, instance=item.images_set.first())
        
        file = request.FILES.getlist('image')
       
        if all([itemsforms.is_valid(), imageforms.is_valid()]):

            item = itemsforms.save(commit=False)
            item.user = request.user
            item.store = store
            item.save()
            
            # we have to delte the existing image before creating new one
            item.images_set.all().delete()
            for i in file:
                Images.objects.create(item=item, image=i)
                
            messages.info(request, f'{item.title} Item updated') 
            url = reverse('jijistore:enter_store', args = [store_id])          
            return redirect(url)
        
        
        messages.error(request, f'Please insert valid data')
        return redirect('edit_item', pk=item_id)
        
    imageforms =ImageForm(instance = item.images_set.first() if item.images_set.exists() else None)
    itemsforms = ItemsForm(instance=item)
    context = {
        'imageforms': imageforms,
        'itemsform':itemsforms,
        'items':item,
        'store':store,
        'item_edit_url':item_edit_url
    }
    return render(request, 'jijiapp/item_update.html', context)

@login_required
def favorite(request):
    user = request.user
    fav = Items.objects.filter(favorite__user=user).order_by('-favorite__date_added')
    
    if request.method == 'POST' and 'favorite_id' in request.POST:
        favorite_id = request.POST['favorite_id']
        item = Items.objects.get(pk = favorite_id)
        favs = Favorite.objects.filter(item=item, user =user)
        if favs:
            favorite = favs.first()
            favorite.date_added =timezone.now()
            favorite.save()
        else:
            add_fav = Favorite.objects.create(item = item, user=user)
        return redirect('favorite')
    
    context = {
        'favs':fav,
    }
    return render(request, 'jijiapp/favorite.html', context)

@login_required   
def delete_fav(request, item_id):
        
    item = get_object_or_404(Items, id=item_id)
   
    delete_f = Favorite.objects.filter(item=item)
    delete_f.delete()
    
    return redirect('favorite')


    
    