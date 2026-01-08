from django.contrib import admin

from .models import (
    Asset,
    Branch,
    BulkIssuance,
    Category,
    InventoryAlert,
    IssueRequest,
    Room,
    Shelf,
    Transformation,
    Zone,
)

admin.site.register(Branch)
admin.site.register(Zone)
admin.site.register(Room)
admin.site.register(Shelf)
admin.site.register(Category)
admin.site.register(Asset)
admin.site.register(InventoryAlert)
admin.site.register(IssueRequest)
admin.site.register(Transformation)
admin.site.register(BulkIssuance)
