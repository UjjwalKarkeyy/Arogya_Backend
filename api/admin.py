from django.contrib import admin
from complainFeedback.models import Complains
from healthContent.models import HealthCategory, MediaContent, ContentRating, ContentView
from doctor.models import Specialty, Doctor

# Register your models here.
admin.site.register(Complains)
admin.site.register(HealthCategory)
admin.site.register(MediaContent)
admin.site.register(ContentRating)
admin.site.register(ContentView)
admin.site.register(Specialty)
admin.site.register(Doctor)
