from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWorkspaceAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_workspace_admin)

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (
            request.user.is_workspace_admin or request.user.role == "MANAGER"
        ))

class IsAdminManagerOrReadOnlyEmployee(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_workspace_admin or request.user.role == "MANAGER":
            return True
        return request.method in SAFE_METHODS or request.method in ("PATCH",)

class IsAdminManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated: return False
        if request.user.is_workspace_admin or request.user.role == "MANAGER": return True
        return request.method in SAFE_METHODS
