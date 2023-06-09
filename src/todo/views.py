from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class ListTask(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)

        return queryset
