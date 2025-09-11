from django.urls import path
from news.feeds import MyProfessionalFeed
from . import views

urlpatterns = [
    path('rss/', MyProfessionalFeed(), name='post_feed'),  # RSS feed FIRST
    path('', views.home, name='home'),
    path('video-test/', views.video_test, name='video_test'),
    path('search/', views.search_posts, name='search_posts'),
    path('about/', views.about_page, name='about'),
    path('privacy/', views.privacy_page, name='privacy'),
    path('contact/', views.contact_page, name='contact'),
    path('music/', views.music_list, name='music_list'),
    path('music/<int:pk>/', views.music_detail, name='music_detail'),
    path('music/<int:pk>/download/', views.download_music, name='download_music'),
    path('videos/', views.video_news_list, name='video_list'),
    path('videos/<slug:slug>/', views.video_news_detail, name='video_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # catch-all LAST
]
