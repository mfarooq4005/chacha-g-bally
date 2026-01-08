from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BulkIssuanceForm, IssueRequestForm, LoginForm, PermissionMatrixForm, TransformationForm
from .models import Asset, InventoryAlert, IssueRequest


ROLE_MODULES = {
    "Principal": ["analytics", "approvals", "alerts"],
    "Coordinator": ["requests", "approvals", "stock"],
    "Storekeeper": ["stock", "issue", "transformation"],
    "Teacher": ["issue", "bulk", "accept"],
}


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "inventory/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    role = request.user.groups.first().name if request.user.groups.exists() else "Teacher"
    modules = ROLE_MODULES.get(role, [])
    alerts = InventoryAlert.objects.filter(resolved_at__isnull=True)[:5]
    low_stock_assets = Asset.objects.filter(quantity_on_hand__lt=10)[:5]
    return render(
        request,
        "inventory/dashboard.html",
        {
            "role": role,
            "modules": modules,
            "alerts": alerts,
            "low_stock_assets": low_stock_assets,
        },
    )


@login_required
@permission_required("auth.change_permission", raise_exception=True)
def permissions_matrix_view(request):
    form = PermissionMatrixForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        permissions = form.cleaned_data["permissions"]
        user.user_permissions.set(permissions)
        messages.success(request, "Permissions updated.")
        return redirect("permissions-matrix")

    if request.GET.get("user"):
        user = get_object_or_404(PermissionMatrixForm.base_fields["user"].queryset, pk=request.GET["user"])
        form.initial = {"user": user, "permissions": user.user_permissions.all()}

    return render(request, "inventory/permissions_matrix.html", {"form": form})


@login_required
def issue_queue_view(request):
    outgoing = IssueRequest.objects.filter(sender=request.user)
    incoming = IssueRequest.objects.filter(receiver=request.user, status="PENDING")
    form = IssueRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        issue = form.save(commit=False)
        issue.sender = request.user
        issue.save()
        messages.success(request, "Issue request created.")
        return redirect("issue-queue")

    return render(
        request,
        "inventory/issue_queue.html",
        {"outgoing": outgoing, "incoming": incoming, "form": form},
    )


@login_required
def accept_issue_view(request, issue_id):
    issue = get_object_or_404(IssueRequest, pk=issue_id, receiver=request.user)
    if issue.status != "PENDING":
        messages.info(request, "Issue already processed.")
        return redirect("issue-queue")

    issue.status = "ACCEPTED"
    issue.accepted_at = timezone.now()
    issue.save()
    issue.asset.quantity_on_hand = max(0, issue.asset.quantity_on_hand - issue.quantity)
    issue.asset.save()
    messages.success(request, "Issue accepted and inventory updated.")
    return redirect("issue-queue")


@login_required
def transformation_view(request):
    form = TransformationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        transformation = form.save(commit=False)
        transformation.created_by = request.user
        transformation.save()
        transformation.raw_material.quantity_on_hand = max(
            0, transformation.raw_material.quantity_on_hand - transformation.consumed_quantity
        )
        transformation.raw_material.save()
        messages.success(request, "Transformation recorded.")
        return redirect("transformations")

    return render(request, "inventory/transformations.html", {"form": form})


@login_required
def bulk_issuance_view(request):
    form = BulkIssuanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        issuance = form.save(commit=False)
        issuance.teacher = request.user
        issuance.save()
        issuance.asset.quantity_on_hand = max(0, issuance.asset.quantity_on_hand - issuance.issued_quantity)
        issuance.asset.save()
        messages.success(request, "Bulk issuance logged.")
        return redirect("bulk-issuance")

    return render(request, "inventory/bulk_issuance.html", {"form": form})
