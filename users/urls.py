from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.utils import email_verification
from users.views import UserCreate, notification, ProfileView, UserListView, \
    UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification,
         name='email-confirm'),
    path('notification/', notification, name='notification'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_block'),
]
