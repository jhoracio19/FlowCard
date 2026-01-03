from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cards.views import RegisterView
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('statements/', include('statements.urls')),
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
        # 1. Formulario para ingresar el correo
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html', # <-- Añade esta línea
        subject_template_name='registration/password_reset_subject.txt' # <-- Opcional: para el asunto
        ),
            name='password_reset'),
    
    # 2. Mensaje de "Correo enviado"
    path('password-reset/done/', 
            auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
            name='password_reset_done'),
    
    # 3. El enlace con token que llega al correo
    path('password-reset-confirm/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
            name='password_reset_confirm'),
    
    # 4. Mensaje de "Contraseña cambiada con éxito"
    path('password-reset-complete/', 
            auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
            name='password_reset_complete'),
]
