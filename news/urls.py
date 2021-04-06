from django.urls import path
from .views import (NewsList, PostDetailView, PostCreateView,
                    PostEditView, PostDeleteView, Search)


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', Search.as_view(), name='search')
]
