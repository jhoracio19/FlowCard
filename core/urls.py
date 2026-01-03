from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cards.views import RegisterView
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Administración de Django
    path('admin/', admin.site.urls),

    # 2. Redirección de la raíz al login
    path('', RedirectView.as_view(url='/login/', permanent=True)),

    # 3. Registro de Aplicaciones con Namespaces (SOLUCIONA EL ERROR AMARILLO)
    path('cards/', include('cards.urls', namespace='cards')),
    path('statements/', include('statements.urls', namespace='statements')),

    # 4. Autenticación (Login, Logout, Registro)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # 5. Recuperación de contraseña (Flujo completo)
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'),
    
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
]