from django.urls import path
from leads import views
urlpatterns = [
    path('', views.Index, name='index')
]