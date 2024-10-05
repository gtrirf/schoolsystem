from django.urls import path
from .views import (
    LessonCreateView, AssignmentCreateView, AssignmentListView,
    SubmissionCreateView, SubmissionUpdateView, AssignmentUpdateView, TeacherSubmissionListView
)

urlpatterns = [
    path('lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('assignments/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/list/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment-update'),
    path('submissions/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionUpdateView.as_view(), name='submission-update'),
    path('submissions/list/', TeacherSubmissionListView.as_view(), name='submission-list'),
]
