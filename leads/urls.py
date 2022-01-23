from django.urls import path
from leads import views
urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('lead_details/<int:pk>/', views.lead_details, name='lead_details'),

]