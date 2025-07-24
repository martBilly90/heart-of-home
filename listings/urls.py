from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_listings_view, name='all-listings'),
    path('edit/<int:pk>/', views.edit_listing_view, name='edit-listing'),
    path('<int:pk>/', views.listing_detail_view, name='listing-detail'),
    path('agents/', views.agents_view, name='agents'),
    path('create/', views.create_listing_view, name='create-listing'),
    path('delete/<int:pk>/', views.delete_listing_view, name='delete-listing'),
    path('message/send/<int:listing_pk>/', views.send_message_view, name='send-message'),
]
