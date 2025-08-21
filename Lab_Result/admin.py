from django.contrib import admin
from .models import LabTest, Hospital, LabReport, LabResultValue

# Define an inline for the LabResultValue model
class LabResultValueInline(admin.TabularInline):
    model = LabResultValue
    extra = 10  # This adds 10 empty forms for new results
    fields = ['sub_test_name', 'value', 'unit', 'reference_range']

# Create a ModelAdmin for LabReport to include the inline
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'test', 'hospital', 'date', 'status')
    inlines = [LabResultValueInline]

# Register the models with their new admin classes
admin.site.register(LabTest)
admin.site.register(Hospital)
admin.site.register(LabReport, LabReportAdmin)

# The LabResultValue model is managed via the inline, but you can keep
# this registration if you want a standalone admin page for it as well.
admin.site.register(LabResultValue)