from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.db import models
from .models import Task, CustomUser
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsSuperuserOrOwner
from django.contrib.auth.hashers import make_password
import base64


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(
            models.Q(user=user) | 
            models.Q(is_superuser_task=True, visible_to_all=True) |
            models.Q(is_superuser_task=True, visible_to=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_superuser_task=self.request.user.is_superuser)

    def perform_update(self, serializer):
        if self.request.user.is_superuser or serializer.instance.user == self.request.user:
            serializer.save()
        else:
            raise permissions.PermissionDenied("No tienes permiso para editar esta tarea.")

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise permissions.PermissionDenied("Solo el superusuario puede eliminar tareas.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()

    def perform_update(self, serializer):
        password = serializer.validated_data.get('password')
        if password and password != '********':
            serializer.validated_data['password'] = make_password(password)
        elif 'password' in serializer.validated_data:
            del serializer.validated_data['password']
        serializer.save()

    @action(detail=True, methods=['get'])
    def get_user_data(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        data = serializer.data
        data['password'] = base64.b64encode('placeholder'.encode()).decode()
        return Response(data)

    def get_queryset(self):
        return CustomUser.objects.exclude(id=self.request.user.id)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)