from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UpdateSettingsView, UpdateTopicsView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', UpdateSettingsView.as_view(), name='update_settings'),
    path('topics/', UpdateTopicsView.as_view(), name='update_topics'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
]
