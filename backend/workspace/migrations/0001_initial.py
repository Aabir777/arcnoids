import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
      migrations.CreateModel(name="Client",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),("updated_at",models.DateTimeField(auto_now=True)),
        ("name",models.CharField(max_length=160)),("company",models.CharField(blank=True,max_length=180)),("email",models.EmailField(blank=True,max_length=254)),("phone",models.CharField(blank=True,max_length=40)),
        ("status",models.CharField(choices=[("PROSPECT","Prospect"),("ACTIVE","Active"),("ON_HOLD","On hold"),("COMPLETED","Completed")],default="PROSPECT",max_length=12)),("notes",models.TextField(blank=True)),
        ("created_by",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="created_clients",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Enquiry",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),("updated_at",models.DateTimeField(auto_now=True)),
        ("name",models.CharField(max_length=160)),("email",models.EmailField(blank=True,max_length=254)),("company",models.CharField(blank=True,max_length=180)),("service",models.CharField(blank=True,max_length=160)),("message",models.TextField(blank=True)),
        ("stage",models.CharField(choices=[("NEW","New"),("CONTACTED","Contacted"),("PROPOSAL","Proposal sent"),("WON","Won"),("LOST","Lost")],default="NEW",max_length=12)),
        ("created_by",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="created_enquiries",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Project",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),("updated_at",models.DateTimeField(auto_now=True)),
        ("name",models.CharField(max_length=180)),("description",models.TextField(blank=True)),("status",models.CharField(choices=[("PLANNING","Planning"),("IN_PROGRESS","In progress"),("REVIEW","Review"),("COMPLETED","Completed"),("ON_HOLD","On hold")],default="PLANNING",max_length=16)),("due_date",models.DateField(blank=True,null=True)),
        ("client",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="projects",to="workspace.client")),("created_by",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="created_projects",to=settings.AUTH_USER_MODEL)),("members",models.ManyToManyField(blank=True,related_name="assigned_projects",to=settings.AUTH_USER_MODEL))]),
      migrations.CreateModel(name="Task",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("created_at",models.DateTimeField(auto_now_add=True)),("updated_at",models.DateTimeField(auto_now=True)),
        ("title",models.CharField(max_length=220)),("description",models.TextField(blank=True)),("status",models.CharField(choices=[("TODO","To do"),("IN_PROGRESS","In progress"),("DONE","Done")],default="TODO",max_length=16)),("due_date",models.DateField(blank=True,null=True)),
        ("assigned_to",models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name="workspace_tasks",to=settings.AUTH_USER_MODEL)),("created_by",models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name="created_tasks",to=settings.AUTH_USER_MODEL)),("project",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="tasks",to="workspace.project"))])
    ]
