from django.urls import path

from surf_shed.booking import views

app_name = "booking"

urlpatterns = [
    path("book/", view=views.new_booking, name="new_booking"),
    path("cancel/", view=views.cancel_booking, name="cancel_booking"),
]

htmx_patterns = [
    path(
        "book/update_time_and_date_select/",
        views.update_time_and_date_select,
        name="update-time-and-date-select-view",
    ),
    path("book/update_check_out/", views.update_check_out, name="update-checkout-view"),
    path("book/do_booking/", views.do_booking, name="do-booking"),
    path("cancel/cancel_booking/", views.cancel_booking, name="cancel-booking"),
    path(
        "cancel/do_cancel_booking/", views.do_cancel_booking, name="do-cancel-booking"
    ),
]

urlpatterns += htmx_patterns
