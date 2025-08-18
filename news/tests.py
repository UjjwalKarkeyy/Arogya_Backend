from django.test import TestCase
from rest_framework.test import APIClient
from .models import HealthFAQ, Tag, Category
from django.urls import reverse