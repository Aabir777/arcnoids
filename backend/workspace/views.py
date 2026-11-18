from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.permissions import IsAdminOrManager, IsAdminManagerOrReadOnlyEmployee, IsWorkspaceAdmin
from accounts.serializers import UserSerializer, TeamCreateSerializer
from .models import Client, Project, Task, Enquiry
from .serializers import ClientSerializer, ProjectSerializer, TaskSerializer, EnquirySerializer
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class=ClientSerializer
    permission_classes=[IsAuthenticated,IsAdminOrManager]
    def get_queryset(self): return Client.objects.all().order_by("-created_at")
    def perform_create(self,serializer): serializer.save(created_by=self.request.user)
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class=ProjectSerializer
    permission_classes=[IsAuthenticated,IsAdminManagerOrReadOnlyEmployee]
    def get_queryset(self):
        qs=Project.objects.select_related("client").prefetch_related("members").order_by("-created_at")
        if self.request.user.is_workspace_admin or self.request.user.role=="MANAGER": return qs
        return qs.filter(members=self.request.user).distinct()
    def perform_create(self,serializer):
        if not (self.request.user.is_workspace_admin or self.request.user.role=="MANAGER"): raise PermissionDenied("Only admins and managers can create projects.")
        serializer.save(created_by=self.request.user)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class=TaskSerializer
    permission_classes=[IsAuthenticated,IsAdminManagerOrReadOnlyEmployee]
    def get_queryset(self):
        qs=Task.objects.select_related("project","assigned_to","project__client").order_by("-created_at")
        if self.request.user.is_workspace_admin or self.request.user.role=="MANAGER": return qs
        return qs.filter(assigned_to=self.request.user)
    def perform_create(self,serializer):
        if not (self.request.user.is_workspace_admin or self.request.user.role=="MANAGER"): raise PermissionDenied("Only admins and managers can create tasks.")
        serializer.save(created_by=self.request.user)
    def perform_update(self,serializer):
        if self.request.user.role=="EMPLOYEE" and not self.request.user.is_workspace_admin:
            if set(self.request.data.keys())-{"status"}: raise PermissionDenied("Employees can update task status only.")
        serializer.save()
class EnquiryViewSet(viewsets.ModelViewSet):
    serializer_class=EnquirySerializer
    permission_classes=[IsAuthenticated,IsAdminOrManager]
    def get_queryset(self): return Enquiry.objects.all().order_by("-created_at")
    def perform_create(self,serializer): serializer.save(created_by=self.request.user)
class TeamViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsWorkspaceAdmin]
    def get_queryset(self): return User.objects.all().order_by("date_joined")
    def get_serializer_class(self): return TeamCreateSerializer if self.action=="create" else UserSerializer
    def perform_destroy(self,instance):
        if instance.pk==self.request.user.pk: raise PermissionDenied("You cannot deactivate your own owner account.")
        instance.is_active=False
        instance.save(update_fields=["is_active"])
