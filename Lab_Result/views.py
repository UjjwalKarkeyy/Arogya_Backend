from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import LabTest, Hospital, LabReport
from .serializers import LabTestSerializer, HospitalSerializer, LabReportSerializer

class LabTestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class LabReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LabReportSerializer

    def get_queryset(self):
        hospital_id = self.request.query_params.get('hospital_id')
        test_name = self.request.query_params.get('test_name')

        if hospital_id and test_name:
            lab_test = get_object_or_404(LabTest, name=test_name)
            return LabReport.objects.filter(hospital_id=hospital_id, test=lab_test)
        
        return LabReport.objects.all()