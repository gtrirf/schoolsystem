from django.urls import path
from . import views

urlpatterns = [
    path('my-exams/', views.ExamsView.as_view(), name='exams'),
    path('exam-results/<int:exam_id>/', views.ExamResultView.as_view(), name='exam_results'),
]
