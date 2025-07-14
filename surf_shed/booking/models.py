"""Database models for the booking app."""

import random
import string

from django.core.exceptions import ValidationError
from django.db import models


class BookingItem(models.Model):
    class State(models.IntegerChoices):
        BOOKABLE = 1, "BOOKABLE"
        BROKEN = 2, "BROKEN"
        NEED_REPAIR = 3, "NEED_REPAIR"
        IS_NO_MORE = 4, "IS_NO_MORE"

    class Category(models.IntegerChoices):
        NOT_SPECIFIED = 1, "NOT_SPECIFIED"
        BEGINNER_BOARD = 2, "BEGINNER_BOARD"
        INTERMEDIATE_BOARD = 3, "INTERMEDIATE_BOARD"
        ADVANCED_BOARD = 4, "ADVANCED_BOARD"
        SUP = 5, "SUP"
        OTHER = 6, "OTHER"

    item_name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, default="")
    item_category = models.PositiveSmallIntegerField(
        choices=Category.choices,
        default=Category.NOT_SPECIFIED,
    )
    item_state = models.PositiveSmallIntegerField(
        choices=State.choices,
        default=State.BOOKABLE,
    )
    item_size_liter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item_name


class BookingRecord(models.Model):
    booked_item = models.ForeignKey(BookingItem, on_delete=models.CASCADE)
    booked_by = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    reserved_start_time = models.DateTimeField("time booking begins")
    reserved_end_time = models.DateTimeField("time booking ends")

    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        null=False,  # Temporarily allow NULLs
        editable=False,
        blank=True,
        db_index=True,
    )

    def __str__(self):
        return (
            f"{self.booked_item}: {self.date} "
            f"from {self.reserved_start_time} "
            f"to {self.reserved_end_time}"
        )

    def save(self, *args, **kwargs):
        self.full_clean()  # Calls clean() to validate before saving
        if not self.booking_reference:
            self.booking_reference = self.generate_unique_booking_reference()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Check for time range overlap
        overlapping_bookings = BookingRecord.objects.filter(
            booked_item=self.booked_item,
            date=self.date,
            reserved_start_time__lt=self.reserved_end_time,
            reserved_end_time__gt=self.reserved_start_time,
        )

        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            error_msg = "This booking time overlaps with an existing booking."
            raise ValidationError(error_msg)

    def generate_unique_booking_reference(self):
        """
        Generates a booking reference in the format:
        ABCDEF
        """

        def generate():
            """generate a reference"""
            suffix = "".join(random.choices(string.ascii_uppercase, k=6))  # noqa: S311
            return f"{suffix}"

        reference = generate()

        while BookingRecord.objects.filter(booking_reference=reference).exists():
            reference = generate()

        return reference
