from django.conf import settings
from django.db import models
class Timestamped(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: abstract=True
class Client(Timestamped):
    class Status(models.TextChoices):
        PROSPECT="PROSPECT","Prospect"
        ACTIVE="ACTIVE","Active"
        ON_HOLD="ON_HOLD","On hold"
        COMPLETED="COMPLETED","Completed"
    name=models.CharField(max_length=160)
    company=models.CharField(max_length=180,blank=True)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=40,blank=True)
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.PROSPECT)
    notes=models.TextField(blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_clients")
    def __str__(self): return self.company or self.name
class Project(Timestamped):
    class Status(models.TextChoices):
        PLANNING="PLANNING","Planning"
        IN_PROGRESS="IN_PROGRESS","In progress"
        REVIEW="REVIEW","Review"
        COMPLETED="COMPLETED","Completed"
        ON_HOLD="ON_HOLD","On hold"
    name=models.CharField(max_length=180)
    client=models.ForeignKey(Client,on_delete=models.PROTECT,related_name="projects")
    description=models.TextField(blank=True)
    status=models.CharField(max_length=16,choices=Status.choices,default=Status.PLANNING)
    due_date=models.DateField(null=True,blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_projects")
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="assigned_projects")
    def __str__(self): return self.name
class Task(Timestamped):
    class Status(models.TextChoices):
        TODO="TODO","To do"
        IN_PROGRESS="IN_PROGRESS","In progress"
        DONE="DONE","Done"
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="tasks")
    title=models.CharField(max_length=220)
    description=models.TextField(blank=True)
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="workspace_tasks")
    status=models.CharField(max_length=16,choices=Status.choices,default=Status.TODO)
    due_date=models.DateField(null=True,blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_tasks")
    def __str__(self): return self.title
class Enquiry(Timestamped):
    class Stage(models.TextChoices):
        NEW="NEW","New"
        CONTACTED="CONTACTED","Contacted"
        PROPOSAL="PROPOSAL","Proposal sent"
        WON="WON","Won"
        LOST="LOST","Lost"
    name=models.CharField(max_length=160)
    email=models.EmailField(blank=True)
    company=models.CharField(max_length=180,blank=True)
    service=models.CharField(max_length=160,blank=True)
    message=models.TextField(blank=True)
    stage=models.CharField(max_length=12,choices=Stage.choices,default=Stage.NEW)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_enquiries")
    def __str__(self): return self.name
