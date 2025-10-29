from django.urls import path
from resumes.views import ResumeListCreateView, ResumeDetailView

urlpatterns = [
    path('api/v3/resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('api/v3/resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
]