from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='reg_pg'),
    path('login/', views.AuthView.as_view(), name='login_pg'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_pg'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('accounts/password/change/', views.UserPassChangeView.as_view(), name='password_change'),
    path('password_reset/', views.UserPassResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.UserPassResetConfirmView.as_view(), name='password_reset_confirm')
]