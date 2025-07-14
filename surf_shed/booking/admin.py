from django.contrib import admin

from surf_shed.booking.models import BookingItem
from surf_shed.booking.models import BookingRecord

# Register your models here.

admin.site.register(BookingItem)


@admin.register(BookingRecord)
class YourModelAdmin(admin.ModelAdmin):
    readonly_fields = ["booking_reference"]
