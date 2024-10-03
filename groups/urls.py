from django.urls import path
from .views import GroupListView, GroupDetailView, AddStudentsToGroupView, RemoveStudentsFromGroupView

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:id>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/add-students/', AddStudentsToGroupView.as_view(), name='add-students'),
    path('groups/<int:group_id>/remove-students/', RemoveStudentsFromGroupView.as_view(), name='remove-students'),
]
