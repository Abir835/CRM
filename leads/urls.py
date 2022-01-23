from django.urls import path
from leads import views
urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('lead_details/<int:pk>/', views.lead_details, name='lead_details'),
    path('lead_create/', views.lead_create, name='lead_create'),
    path('lead_update/<int:pk>/', views.lead_update, name='lead_update'),

]