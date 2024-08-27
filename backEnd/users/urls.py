from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UpdateSettingsView, UpdateTopicsView, UserDetailView

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/settings/', UpdateSettingsView.as_view(), name='update_settings'),
    path('user/topics/', UpdateTopicsView.as_view(), name='update_topics'),
    path('user/me/', UserDetailView.as_view(), name='user_detail'),
]
