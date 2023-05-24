from django import forms

class storeForm(forms.Form):
    name = forms.CharField(label='Your Store name')
    discription = forms.CharField(label='description')
    # create_date= forms.DateField(widget = forms.DateInput)
    location = forms.CharField(label='location')
    
    logo = forms.ImageField()