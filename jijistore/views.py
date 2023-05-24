from django.shortcuts import render, redirect, get_object_or_404
from jijiapp.models import Items, Store, Images
from jijistore.forms import storeForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


# this views create store
@login_required
def storelist(request):
    user = request.user
    created_by_you = Store.objects.filter(author =user)
    if request.method == 'POST':
        form = storeForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('discription')
            # date_uploaded = form.cleaned_data.get('create_date')
            location = form.cleaned_data.get('location')
            logo = form.cleaned_data.get('logo')
            
            if Store.objects.filter(name = name).exists():
                messages.error(request, f'{name} Store already exist')
                return redirect('jijistore:storelist')
            
            store= Store.objects.create(author=user, name = name, discription=description,
                    location=location,logo =logo)
           
            
            messages.success(request, f'The Store with name {name} created successful')
            return redirect('jijistore:storelist')
        messages.error(request, f'Invalid data')
        return redirect('jijistore:storelist')
    form = storeForm()
    context = {
        'form':form,
        'created_by_you':created_by_you,
    }
    return render(request, 'jijistore/store.html', context)
@login_required
def all_store(request):
    store = Store.objects.all()
    
    context = {
        'stores':store,
    }
    return render(request, 'jijistore/all_store.html', context)
@login_required
def enter_store(request, store):
    
    try:
        stor = Store.objects.get(id=store)
        all_items = stor.items_set.all()
    except Store.DoesNotExist:
        all_items = None
        stor =None
        # all_items = stor.items_set.all()

    context = {
        'details':stor,
        'items':all_items,
    }
    return render(request, 'jijistore/store_detail.html', context)
@login_required
def edit_store(request, store_id):
    
    store = get_object_or_404(Store, name=store_id)
    if request.method == 'POST':
        form = storeForm(request.POST, request.FILES, 
                         initial={
                        'name': store.name,
                        'discription': store.discription,
                        'location': store.location,
                        'logo': store.logo,})
        if form.is_valid():
            store.name = form.cleaned_data.get('name')
            store.discription = form.cleaned_data.get('discription')
            store.location = form.cleaned_data.get('location')
            store.logo = form.cleaned_data.get('logo')
            
            store.save()
            messages.success(request, 'Store updated')
            return redirect('jijistore:all_store')
        messages.error(request, 'Invalid input')
        reverse('edit_store', args = [store_id])
        
    # initial_values = {
    #         'name': store.name,
    #         'discription': store.discription,
    #         'location': store.location,
    #         'logo': store.logo,
    #     }
    form = storeForm(initial={
            'name': store.name,
            'discription': store.discription,
            'location': store.location,
            'logo': store.logo,
        })
    context = {
        'form':form,
        'store':store,
    }
    return render(request, 'jijistore/store_update.html', context)
            
        
    