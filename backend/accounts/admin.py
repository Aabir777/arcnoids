from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class WorkspaceUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Workspace access", {"fields": ("role", "must_change_password")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Workspace access", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_active", "is_staff")
