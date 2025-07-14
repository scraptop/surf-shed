from django.urls import path

from surf_shed.booking.views import cancel_booking
from surf_shed.booking.views import new_booking

app_name = "booking"

urlpatterns = [
    path("book/", view=new_booking, name="new_booking"),
    path("cancel/", view=cancel_booking, name="cancel_booking"),
]

htmx_patterns = []

urlpatterns += htmx_patterns
