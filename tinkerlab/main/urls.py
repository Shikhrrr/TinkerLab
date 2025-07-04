
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('search/', views.search_items, name='search'),
    path('item/<str:item_id>/', views.view_item, name='view_item'),
    path('book/<str:item_id>/', views.book_item, name='book_item'),

    path('requests/', views.request_status, name='request_status'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # admin panel routes
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add-item/', views.add_item, name='add_item'),
    path('admin-panel/edit-item/<str:item_id>/', views.edit_item, name='edit_item'),
    path('admin-panel/delete-item/<str:item_id>/', views.delete_item, name='delete_item'),
    path('admin-panel/requests/', views.pending_requests, name='pending_requests'),
    path('admin-panel/request/<int:req_id>/respond/', views.respond_request, name='respond_request'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
