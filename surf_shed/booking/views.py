from django.shortcuts import render


def new_booking(request):
    context = {}
    return render(request, "booking/new_booking.html", context)


def cancel_booking(request):
    context = {}
    return render(request, "booking/cancel_booking.html", context)
