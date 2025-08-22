from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status

from .models import Registration
from .serializers import RegistrationSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    # Require authentication for health camp registration
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        return (
            Registration.objects.filter(user=user)
            .select_related("campaign")
            .prefetch_related("campaign__vaccines", "campaign__medicines")
        )

    def create(self, request, *args, **kwargs):
        # Validate input first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Resolve user - require authentication for health camp registration
        user = request.user
        if not user.is_authenticated:
            raise NotAuthenticated("Authentication credentials were not provided.")

        campaign = serializer.validated_data.get("campaign")
        if campaign is None:
            raise ValidationError({"campaign": ["This field is required."]})

        # Idempotent behavior: if already exists, return 200 with existing record
        existing = (
            Registration.objects.filter(user=user, campaign=campaign)
            .select_related("campaign")
            .prefetch_related("campaign__vaccines", "campaign__medicines")
            .first()
        )
        if existing:
            existing_ser = self.get_serializer(existing)
            body = {"detail": "You are already registered for this campaign.", "data": existing_ser.data}
            return Response(body, status=status.HTTP_200_OK)

        # Create new
        try:
            instance = serializer.save(user=user)
        except IntegrityError:
            # In rare race conditions, fall back to fetching existing and return 200
            existing = (
                Registration.objects.filter(user=user, campaign=campaign)
                .select_related("campaign")
                .prefetch_related("campaign__vaccines", "campaign__medicines")
                .first()
            )
            if existing:
                existing_ser = self.get_serializer(existing)
                body = {"detail": "You are already registered for this campaign.", "data": existing_ser.data}
                return Response(body, status=status.HTTP_200_OK)
            # If truly another integrity error
            raise

        out = self.get_serializer(instance)
        headers = self.get_success_headers(out.data)
        return Response({"detail": "Registration successful.", "data": out.data}, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)