from django.contrib import admin

from company.models import Employee, Room


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ["age"]
    list_display = ["first_name", "last_name", "position", "experience", "age"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "capacity"]

