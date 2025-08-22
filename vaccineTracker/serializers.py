import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Vaccine, UserVaccineRecord


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ["id", "name", "manufacturer", "max_doses", "dose_interval_days"]


class UserVaccineRecordSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.CharField(source="vaccine.name", read_only=True)
    next_due_date = serializers.DateField(read_only=True)
    next_dose_number = serializers.IntegerField(read_only=True)

    patient_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    vaccine_id = serializers.UUIDField(write_only=True, required=False)
    dose_number = serializers.IntegerField(required=False)
    
    date_given = serializers.DateField(required=False, allow_null=True)
    administered_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = UserVaccineRecord
        fields = [
            "id", "user", "patient_name", "vaccine",
            "vaccine_id", "vaccine_name", "dose_number",
            "date_given", "administered_by", "notes", "verified",
            "created_at", "next_due_date", "next_dose_number",
        ]
        read_only_fields = ["id", "user", "vaccine", "verified", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["patient_name"] = instance.patient_name 

        vax = instance.vaccine
        if vax.max_doses and instance.dose_number < vax.max_doses:
            if instance.date_given and vax.dose_interval_days:
                next_date = instance.date_given + datetime.timedelta(days=vax.dose_interval_days)
                data["next_due_date"] = next_date
                data["next_dose_number"] = instance.dose_number + 1
        return data

    def validate(self, attrs):
        request = self.context.get("request")
        user = None

        patient_name = attrs.pop("patient_name", "").strip()
        
        if request and request.user and request.user.is_authenticated:
            user = request.user
            if patient_name:
                attrs["patient_name"] = patient_name
            else:
                attrs["patient_name"] = user.username
        else:
            raise serializers.ValidationError(
                {"user": "Missing user. Provide patient_name, or authenticate."}
            )

        if not self.instance:
            vaccine_id = attrs.get("vaccine_id")
            dose_number = attrs.get("dose_number")

            if not vaccine_id:
                raise serializers.ValidationError({"vaccine_id": "This field is required for creating a record."})
            if dose_number is None:
                raise serializers.ValidationError({"dose_number": "This field is required for creating a record."})

            try:
                vaccine = Vaccine.objects.get(id=vaccine_id)
            except Vaccine.DoesNotExist:
                raise serializers.ValidationError({"vaccine_id": "Invalid vaccine id."})

            if dose_number < 1:
                raise serializers.ValidationError({"dose_number": "Dose number must be 1 or greater."})
            if vaccine.max_doses and dose_number > vaccine.max_doses:
                raise serializers.ValidationError(
                    {"dose_number": f"Cannot exceed the maximum of {vaccine.max_doses} doses for this vaccine."}
                )

            if UserVaccineRecord.objects.filter(user=user, vaccine=vaccine, dose_number=dose_number).exists():
                raise serializers.ValidationError(
                    {"dose_number": "This dose number already exists for this user and vaccine."}
                )

            attrs["vaccine"] = vaccine
        else:
            pass

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        validated_data.pop("vaccine_id", None)
        return UserVaccineRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.verified:
            raise serializers.ValidationError("Cannot edit a verified record.")

        validated_data.pop("vaccine_id", None)
        validated_data.pop("dose_number", None)
        validated_data.pop("user", None)

        patient_name = validated_data.get("patient_name")
        if patient_name is None or patient_name.strip() == "":
            validated_data["patient_name"] = instance.user.username

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
