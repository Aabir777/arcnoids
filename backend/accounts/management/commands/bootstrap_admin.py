import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accounts.models import User
class Command(BaseCommand):
    help = "Create the first Arcnoids workspace owner from environment variables."
    def handle(self, *args, **options):
        if User.objects.filter(role=User.Role.ADMIN,is_active=True).exists():
            self.stdout.write(self.style.WARNING("An active workspace admin already exists; no changes made.")); return
        username=os.getenv("ADMIN_USERNAME","").strip(); email=os.getenv("ADMIN_EMAIL","").strip(); password=os.getenv("ADMIN_PASSWORD","")
        if not username or not email or len(password)<12: raise CommandError("Set ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD (at least 12 characters).")
        if User.objects.filter(username=username).exists(): raise CommandError("That ADMIN_USERNAME already exists.")
        try:
            validate_password(password)
        except ValidationError as exc:
            raise CommandError("; ".join(exc.messages))
        user=User.objects.create_superuser(username=username,email=email,password=password,role=User.Role.ADMIN)
        self.stdout.write(self.style.SUCCESS(f"Workspace owner created: {user.username}"))
