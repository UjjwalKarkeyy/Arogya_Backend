from django.db import models
import uuid

class LabTest(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Hospital(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name

class LabReport(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.CharField(max_length=100)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=[('Ready', 'Ready'), ('Processing', 'Processing')])

    def __str__(self):
        return f"Report for {self.patient_id} - {self.test.name}"

class LabResultValue(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(LabReport, related_name='results', on_delete=models.CASCADE)
    sub_test_name = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True, null=True)
    reference_range = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.sub_test_name} - {self.value} {self.unit or ''}"