from rest_framework.serializers import (
    Serializer, ModelSerializer, SerializerMethodField, EmailField, ValidationError, PrimaryKeyRelatedField
)

from company.models import Employee, Reservation, Room


class EmployeeSerializer(ModelSerializer):
    position = CharField(write_only=True)
    class Meta:
        model = Employee
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:
        # Validate that the email domain is 'gmail'
        if (email := attrs.get("email")) and not "@gmail" in email:
            raise ValidationError("Employee's email must belong to the 'gmail' domain.")
        
        # Validate that employee's age is a number bigger than his experience
        if (experience := attrs.get("experience") and "date_of_birth" in attrs.keys()):
            employee = Employee(**attrs)
            if employee.age < experience:
                raise ValidationError("An employee should not have more years of experience, than years of living..")
        
        return attrs


class RoomSerializer(ModelSerializer):
    title = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_title(self, obj: Room) -> str:
        return f"{obj.name} ({obj.capacity})"


class AttendeesSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email"]


class ReservationSerializer(ModelSerializer):
    host_employee_email = EmailField(source="host.email", read_only=True)
    attendees = AttendeesSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:
        # Validate that meetings do not overlap
        colliding_reservation_count = Reservation.objects.filter(
            room=attrs["room"], 
            reserved_to__gte=attrs["reserved_from"],
            reserved_from__lte=attrs["reserved_to"]
        ).count()

        if colliding_reservation_count > 0:
            raise ValidationError("The meeting room is already booked for the provided period.")
        
        return attrs
    
    def create(self, validated_data: dict) -> dict:
        if request := self.context.get("request"):
            ip_address = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
            if ip_address:
                validated_data["creator_ip"] = ip_address
        return super().create(validated_data)


class AttendeeAddSerializer(Serializer):
    employee_id = PrimaryKeyRelatedField(queryset=Employee.objects.all())

    def validate(self, attrs: dict) -> dict:
        reservation = self.context["reservation"]
        if reservation.attendees.count() >= reservation.room.capacity:
            raise ValidationError("Room capacity has been reached, additional attendee can not be added.")
        return attrs


    def update(self, instance: Reservation, validated_data: dict):
        employee = validated_data['employee_id']
        instance.attendees.add(employee)
        return instance
