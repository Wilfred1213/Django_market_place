
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jijiapp.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('jijiapp.urls')),
    path('store/', include('jijistore.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='jijiapp/registration/login.html', authentication_form=LoginForm), name='login'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('inbox/', include('jijiapp.routing')),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='jijiapp/registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='jijiapp/registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='jijiapp/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='jijiapp/registration/password_reset_complete.html'), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
