import datetime
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Vaccine, UserVaccineRecord
from .serializers import VaccineSerializer, UserVaccineRecordSerializer

class VaccineViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    (4) Get the list of vaccine details from vaccines table.
    """
    queryset = Vaccine.objects.all().order_by("name")
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class UserVaccineRecordViewSet(viewsets.ModelViewSet):
    """
    (1) List vaccinated with filters (name, date_given, isVerified) + next_due_date for max_doses == 2.
    (2) POST add vaccination with validations & optional fields.
    (3) Edit/remove records only if not verified.
    """
    queryset = UserVaccineRecord.objects.select_related("user", "vaccine").all()
    serializer_class = UserVaccineRecordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)

        name = self.request.query_params.get("name")
        date_given = self.request.query_params.get("date_given")
        is_verified = self.request.query_params.get("isVerified")

        if name:
            qs = qs.filter(
                patient_name__icontains=name
            ) | qs.filter(
                vaccine__name__icontains=name
            )

        if date_given:
            qs = qs.filter(date_given=date_given)

        if is_verified is not None:
            val = is_verified.lower() in ["true", "1", "yes"]
            qs = qs.filter(verified=val)

        return qs.order_by("-date_given", "-created_at")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.verified:
            return Response(
                {"detail": "Cannot delete a verified record."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def notifications(self, request):
        user = request.user

        user_records = (
            UserVaccineRecord.objects
            .filter(user=user)
            .select_related("vaccine")
        )

        latest_per_vaccine = {}
        for rec in user_records:
            key = rec.vaccine_id
            prev = latest_per_vaccine.get(key)
            if (prev is None) or (rec.dose_number > prev["dose_number"]) or (
                rec.dose_number == prev["dose_number"]
                and (rec.date_given or datetime.date.min) > (prev["date_given"] or datetime.date.min)
            ):
                latest_per_vaccine[key] = {
                    "vaccine": rec.vaccine,
                    "dose_number": rec.dose_number,
                    "date_given": rec.date_given,
                }

        notifications = []
        for info in latest_per_vaccine.values():
            vaccine = info["vaccine"]
            last_dose = info["dose_number"]
            last_date = info["date_given"]

            if vaccine.max_doses and last_dose < vaccine.max_doses:
                next_dose = last_dose + 1
                next_due = None
                if vaccine.dose_interval_days and last_date:
                    next_due = last_date + datetime.timedelta(days=vaccine.dose_interval_days)

                notifications.append({
                    "vaccine_id": str(vaccine.id),
                    "vaccine_name": vaccine.name,
                    "next_dose_number": next_dose,
                    "next_due_date": next_due,
                })

        return Response(notifications, status=200)
