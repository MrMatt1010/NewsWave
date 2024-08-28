from django.urls import path
from . import views

urlpatterns = [
    path('fetch-news/', views.fetch_and_store_articles, name='fetch-news'),
    path('test/', views.test_endpoint, name='test'),
]