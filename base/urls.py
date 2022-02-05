from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>/', views.update_room, name='update_room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete_room'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('create-comment/', views.create_comment, name='create_comment'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete_comment'),

    # user urls
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('update-user/', views.update_user, name='update_user'),

    # topics
    path('topics/', views.topics_page, name='topics_page'),

    #activity
    path('activity/', views.activity_page, name='activity_page'),
]