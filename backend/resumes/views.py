from rest_framework import generics
from .models import Resume
from .serializers import ResumeSerializer

class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
