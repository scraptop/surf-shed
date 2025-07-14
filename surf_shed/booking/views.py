from datetime import UTC
from datetime import datetime
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from icecream import ic

from surf_shed.booking.models import BookingItem
from surf_shed.booking.models import BookingRecord


def new_booking(request):
    """Index view for Boka/ new booking."""
    boards = BookingItem.objects.all().order_by("id")  # type: ignore[attr-defined]

    context = {
        "boards": boards,
    }
    return render(request, "booking/new_booking.html", context)


def index(request):
    boards = BookingItem.objects.all().order_by("id")  # type: ignore[attr-defined]

    context = {
        "boards": boards,
    }
    return render(request, "booking/index.html", context)


# @login_required
def do_cancel_booking(request):
    """Cancel booking and update database."""
    if request.method != "POST":
        return HttpResponseForbidden("Stop it!")

    ic(request.POST.keys())
    password = request.POST.get("auth_password")  # Field from your form
    booking_number = request.POST.get("full_code")  # Your hidden input

    # Assuming only one user exists
    user_model = get_user_model()
    user = user_model.objects.get(username="linsurf")  # or use user.id or email

    user_check = authenticate(request, username=user.username, password=password)

    if not user_check:
        context = {"error_message": "Fel lösenord"}
        return render(request, "booking/partial/on_booking_cancellation.html", context)

    login(request, user_check)

    try:
        item = ic(BookingRecord.objects.get(booking_reference__exact=booking_number))  # type: ignore[attr-defined]
        item.delete()  # type: ignore[attr-defined]
    except BookingRecord.DoesNotExist:  # type: ignore[attr-defined]
        context = {"error_message": f"Ingen bokning hittad för {booking_number}"}
        return render(request, "booking/partial/on_booking_cancellation.html", context)

    context = {}
    return render(request, "booking/partial/on_booking_cancellation.html", context)


def cancel_booking(request):
    """Show cancel booking view."""
    # https://stackoverflow.com/questions/73626180/how-should-i-insert-html-input-data-into-a-django-database
    context = {}
    return render(request, "booking/cancel_booking.html", context)


def do_booking(request):
    """Add booking to database."""
    # https://stackoverflow.com/questions/73626180/how-should-i-insert-html-input-data-into-a-django-database

    if request.method != "POST":
        return HttpResponse(status=400)

    if not request.headers.get("HX-Request"):
        return HttpResponse(status=400)

    # Log on first or die
    password = request.POST.get("auth_password")  # Field from your form
    user_model = get_user_model()
    user = user_model.objects.get(username="linsurf")  # or use user.id or email
    user_check = authenticate(request, username=user.username, password=password)

    if not user_check:
        context = {"error_message": "Fel lösenord"}
        return render(request, "booking/partial/on_booking_confirm.html", context)

    login(request, user_check)

    # Do booking
    try:
        item = ic(BookingItem.objects.get(pk=request.POST.get("board_id")))  # type: ignore[attr-defined]
        time_start = int(request.POST.get("time_data"))
        time_end = ic(int(request.POST.get("time_data_end")))
        time_end = time_end + 1
        date_str = ic(request.POST.get("date_data"))

        _date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)  # type: ignore[arg-type]
        record = BookingRecord.objects.create(  # type: ignore[attr-defined]
            booked_item=item,
            date=_date.date(),
            reserved_start_time=_date.replace(hour=time_start),
            reserved_end_time=_date.replace(hour=time_end),
        )
    except (ValueError, TypeError, BookingItem.DoesNotExist) as e:  # type: ignore[attr-defined]
        ic(f"Could not make a reservation {e=}")
        context = {
            "error_message": "Bokningen misslyckades. Ladda om sidan och försök igen.",
        }
        return render(request, "booking/partial/on_booking_confirm.html", context)

    ic(record.booking_reference)

    context = {"booking_number": record.booking_reference}
    return render(request, "booking/partial/on_booking_confirm.html", context)


def update_check_out(request):
    """Update verification step."""
    if request.method != "POST":
        return HttpResponse(status=400)

    if not request.headers.get("HX-Request"):
        return HttpResponse(status=400)

    board_name = BookingItem.objects.get(pk=request.POST.get("board_id")).item_name  # type: ignore[attr-defined]

    context = {
        "board_id": request.POST.get("board_id"),
        "board_name": board_name,
        "time_data": request.POST.get("time_data"),
        "time_data_start": request.POST.get("selection_start_time"),
        "time_data_end": request.POST.get("selection_end_time"),
        "date_data": request.POST.get("date_data"),
    }

    return render(request, "booking/partial/booking_reservation.html", context)


def check_if_timeslot_is_booked(timeslot: int, booked_timeslots):
    return any(timeslot in range(slot[0], slot[1]) for slot in booked_timeslots)


def compute_day_object(_date, timeslots, bookings):
    day_bookings = bookings.filter(date=_date)
    _booked_timeslots = [
        (booking.reserved_start_time.hour, booking.reserved_end_time.hour)
        for booking in day_bookings
    ]

    timeslots_meta = []
    for timeslot in timeslots:
        booked = check_if_timeslot_is_booked(timeslot, _booked_timeslots)
        timeslots_meta.append({"start_hour": timeslot, "booked": booked})

    return {
        "title": _date.strftime("%A"),
        "date": _date.isoformat(),
        "times": timeslots_meta,
    }


def update_time_and_date_select(request):
    if request.method != "POST":
        return HttpResponse(status=400)

    if not request.headers.get("HX-Request"):
        return HttpResponse(status=400)

    nr_of_days_ahead = 7
    today = datetime.now(tz=UTC).date()
    # Create a list of 7 days starting with today.
    days = [today + timedelta(days=i) for i in range(nr_of_days_ahead)]

    # Times: e.g. every two hours from 6AM to 10PM
    start_hour_pm = 6
    end_hour_pm = 22
    increment_in_hours = 1
    timeslot_1h = list(range(start_hour_pm, end_hour_pm, increment_in_hours))

    # Fetch bookings for the given week
    end_date = today + timedelta(days=nr_of_days_ahead - 1)

    item = ic(BookingItem.objects.get(pk=request.POST.get("board_id")))  # type: ignore[attr-defined]
    bookings = BookingRecord.objects.filter(
        date__gte=today,
        date__lte=end_date,
        booked_item=item,
    )  # type: ignore[attr-defined]

    days_record = [compute_day_object(day, timeslot_1h, bookings) for day in days]

    # Create a dictionary to store bookings by (day, hour) for quick lookup
    booking_lookup = {}
    for booking in bookings:
        key = (booking.date, booking.reserved_start_time.hour)  # Tuple (date, hour)
        booking_lookup[key] = booking  # Store the booking object

    context = {
        "days_record": days_record,  # list of date objects
    }

    context.update(
        {
            "board_id": request.POST.get("board_id"),
            "board_name": request.POST.get("board_name"),
        },
    )

    return render(request, "booking/partial/time_and_date_select.html", context)
