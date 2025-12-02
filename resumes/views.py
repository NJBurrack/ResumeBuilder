from rest_framework import generics, permissions
from .models import Resume
from .serializers import ResumeSerializer
from .permissions import IsOwnerOrReadOnly


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        # Sets the owner of the resume to the logged-in user automatically
        serializer.save(owner=self.request.user)


class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsOwnerOrReadOnly]
