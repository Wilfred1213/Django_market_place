from django.forms import ModelForm
from .models import Items, Images
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from multiupload.fields import MultiFileField, MultiMediaField
# from multiupload.widgets import MultiClearableFileInput


from .models import ConversationMessage, Category



class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-10 rounded-xl border'
            })
        }
        


# class CategoryModelMultipleChoiceField(ModelMultipleChoiceField):
#     def label_from_instance(self, obj):
#         return obj.name

# class ItemsForm(forms.ModelForm):
#     category = CategoryModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = Items
#         exclude = ['user', 'store']


class ItemsForm(ModelForm):
    
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                      widget=forms.SelectMultiple,)


    class Meta:
        model =Items
        exclude = ['user', 'store']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categorys =[(cat.id, cat.name) for cat in Category.objects.all()] 
        self.fields['category'].choices = [('', 'Select a Category')] + categorys   

class ImageForm(forms.ModelForm):
    image = MultiFileField(max_num=5, min_num=1)

    class Meta:
        model = Images
        fields = ['image',]

# class ImageForm(forms.ModelForm):
#     image = MultiFileField(widget=MultiClearableFileInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = Images
#         fields = ['image',]


# class ImageForm(ModelForm):
#     image = forms.ImageField(widget=ClearableFileInput(attrs={'class': 'form-control', "multiple":True}))

#     class Meta:
#         model = Images
#         fields = ['image',]
  
# class ImageForm(ModelForm):
#     image = forms.ImageField(widget =forms.FileInput(attrs  = {'class':'form-control',
#                 "multiple":True}))
    
#     class Meta:
#         model =Images
#         fields = ['image',]
        
# authentication

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': ''
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': ''
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': ''
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': ''
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': ''
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': ''
    }))
    
        
class CommentForm(forms.Form):
    detail = forms.CharField(label='Enter you View')
    
    