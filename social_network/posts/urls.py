from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='main_page'),
    path('group/<slug:slug>/', views.posts, name='group'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
]
