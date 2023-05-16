from django.contrib import admin

from company.models import Employee, Reservation, Room


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = [
        "age",
        "employees_assuming_the_same_position",
        "is_veteran",
        "hosted_reservations_count",
    ]
    list_display = ["first_name", "last_name", "position", "experience", "age"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "capacity"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ["attendees_count"]
    list_display = ["room", "reserved_from", "reserved_to", "host"]
