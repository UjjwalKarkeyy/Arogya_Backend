from django.db import models
from django.contrib.auth.models import User
import uuid

class Vaccine(models.Model):
    """
    Represents a vaccine type (e.g., Pfizer, Moderna, etc.).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=150, blank=True, null=True)
    max_doses = models.PositiveIntegerField(default=1)
    dose_interval_days = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Recommended days between doses (if applicable)."
    )

    def __str__(self):
        return f"{self.name} ({self.manufacturer})" if self.manufacturer else self.name


class UserVaccineRecord(models.Model):
    """
    Stores vaccination details for each user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vaccine_records")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="user_records")
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    dose_number = models.PositiveIntegerField()
    date_given = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=150, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "vaccine", "dose_number")
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.user.username} - {self.vaccine.name} (Dose {self.dose_number})"
