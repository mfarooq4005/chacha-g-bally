from django.conf import settings
from django.db import models
from django.utils import timezone


class Branch(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Zone(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.branch} / {self.name}"


class Room(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.zone} / {self.name}"


class Shelf(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="shelves")
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.room} / Shelf {self.code}"


class Category(models.Model):
    name = models.CharField(max_length=120)
    is_raw_material = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=160)
    sku = models.CharField(max_length=80, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="assets")
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_threshold = models.PositiveIntegerField(default=10)
    shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT, related_name="assets")

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self):
        return self.quantity_on_hand < self.reorder_threshold


class InventoryAlert(models.Model):
    ALERT_TYPES = [
        ("LOW_STOCK", "Low stock"),
        ("HEERA_PHERI", "Heera Pheri"),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="alerts", null=True, blank=True)
    message = models.CharField(max_length=255)
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.message}"


class IssueRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="issues")
    quantity = models.PositiveIntegerField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issued_items")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_items")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    requested_at = models.DateTimeField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset} to {self.receiver} ({self.status})"


class Transformation(models.Model):
    raw_material = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="transformations")
    finished_good_name = models.CharField(max_length=160)
    finished_good_quantity = models.PositiveIntegerField()
    consumed_quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to="transformations/", null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.finished_good_name} ({self.finished_good_quantity})"


class BulkIssuance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="bulk_issuances")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bulk_issued")
    class_name = models.CharField(max_length=120)
    issued_quantity = models.PositiveIntegerField()
    damaged_quantity = models.PositiveIntegerField(default=0)
    wastage_notes = models.TextField(blank=True)
    issued_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.class_name} - {self.asset}"
