import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})

@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_protect
def login_view(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if not user or not user.is_active:
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response({"user": UserSerializer(user).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "Signed out."})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response({"user": UserSerializer(request.user).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def password_change_view(request):
    current = request.data.get("current_password", "")
    new = request.data.get("new_password", "")
    if not request.user.check_password(current):
        return Response({"detail": "Current password is incorrect."}, status=400)
    try:
        validate_password(new, request.user)
    except ValidationError as exc:
        return Response({"detail": list(exc.messages)}, status=400)
    request.user.set_password(new)
    request.user.must_change_password = False
    request.user.save()
    update_session_auth_hash(request, request.user)
    return Response({"detail": "Password updated."})

@api_view(["GET"])
@permission_classes([AllowAny])
def bootstrap_status(request):
    return Response({"ownerConfigured": User.objects.filter(role=User.Role.ADMIN, is_active=True).exists()})
