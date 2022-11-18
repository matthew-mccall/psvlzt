
from django.urls import path

from . import views

app_name = 'custom_ui_tutorial_app'
urlpatterns = [
    path('home/', views.home, name='home'),
]
