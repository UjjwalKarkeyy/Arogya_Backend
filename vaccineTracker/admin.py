from django.contrib import admin
from .models import Vaccine, UserVaccineRecord

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "manufacturer", "max_doses", "dose_interval_days")
    search_fields = ("name", "manufacturer")
    ordering = ("name",)  # safe ordering, since no created_at field


@admin.register(UserVaccineRecord)
class UserVaccineRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "vaccine", "dose_number", "date_given", "verified", "created_at")
    list_filter = ("verified", "vaccine", "dose_number")
    search_fields = ("user__username", "vaccine__name", "patient_name")

    actions = ["verify_records"]

    def verify_records(self, request, queryset):
        updated = queryset.filter(verified=False).update(verified=True)
        self.message_user(request, f"{updated} vaccination record(s) verified successfully.")
    verify_records.short_description = "Verify selected vaccination records"
