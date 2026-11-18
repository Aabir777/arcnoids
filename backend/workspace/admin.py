from django.contrib import admin
from .models import Client, Project, Task, Enquiry
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=("name","company","email","status","created_at")
    search_fields=("name","company","email")
    list_filter=("status",)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=("name","client","status","due_date")
    list_filter=("status",)
    search_fields=("name","client__name")
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=("title","project","assigned_to","status","due_date")
    list_filter=("status",)
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display=("name","company","service","stage","created_at")
    list_filter=("stage",)
