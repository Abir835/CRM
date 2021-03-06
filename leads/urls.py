from django.urls import path
from leads import views
urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('lead_details/<int:pk>/', views.LeadDetailView.as_view(), name='lead_details'),
    path('lead_create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('lead_update/<int:pk>/', views.LeadUpdateView.as_view(), name='lead_update'),
    path('lead_delete/<int:pk>/', views.LeadDeleteView.as_view(), name='lead_delete'),
    path('assign_agent/<int:pk>/', views.AssignAgentView.as_view(), name='assign_agent'),
    path('category', views.CategoryListView.as_view(), name='category'),
    path('category_detail/<int:pk>/', views.CategoryDetailsView.as_view(), name='category_detail'),
    path('category_update/<int:pk>/', views.LeadCategoryUpdate.as_view(), name='category_update'),


]