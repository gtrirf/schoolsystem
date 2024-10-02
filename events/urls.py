from django.urls import path
from .views import EventView, EventRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail')
]
