from django.contrib import admin
from django.urls import path
from inventory import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("permissions/", views.permissions_matrix_view, name="permissions-matrix"),
    path("issues/", views.issue_queue_view, name="issue-queue"),
    path("issues/accept/<int:issue_id>/", views.accept_issue_view, name="accept-issue"),
    path("transformations/", views.transformation_view, name="transformations"),
    path("bulk-issuance/", views.bulk_issuance_view, name="bulk-issuance"),
]
