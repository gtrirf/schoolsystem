from django.urls import path
from . import views


urlpatterns = [
    path('my-xp/', views.RatingView.as_view(), name='my-xp'),
    path('ranking-list/', views.RatingListView.as_view(), name='ranking-list'),
]
