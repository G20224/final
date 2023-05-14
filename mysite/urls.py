from django.urls import path
from . import views

urlpatterns = [
    path('tour/', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('tour/<int:tour_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('about/',views.about, name='about'),
    path('search_results', views.search_results, name='search_results'),
    path('index', views.index),
    path('index/create/', views.create),
    path('index/edit/<int:id>/', views.edit),
    path('index/delete/<int:id>/', views.delete), 
]