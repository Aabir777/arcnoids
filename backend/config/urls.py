from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from workspace.views import ClientViewSet, ProjectViewSet, TaskViewSet, EnquiryViewSet, TeamViewSet
from accounts.views import csrf_token, login_view, logout_view, me_view, password_change_view, bootstrap_status

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="client")
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")
router.register("enquiries", EnquiryViewSet, basename="enquiry")
router.register("team", TeamViewSet, basename="team")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", lambda request: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse({"status": "ok", "service": "arcnoids-api"})),
    path("api/auth/csrf/", csrf_token),
    path("api/auth/login/", login_view),
    path("api/auth/logout/", logout_view),
    path("api/auth/me/", me_view),
    path("api/auth/password/", password_change_view),
    path("api/auth/bootstrap-status/", bootstrap_status),
    path("api/", include(router.urls)),
]
