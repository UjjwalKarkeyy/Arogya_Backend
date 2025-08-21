from rest_framework import serializers
from .models import LabTest, Hospital, LabReport, LabResultValue

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class LabResultValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Add this to handle updates

    class Meta:
        model = LabResultValue
        fields = ['id', 'sub_test_name', 'value', 'unit', 'reference_range']

class LabReportSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    hospital_address = serializers.CharField(source='hospital.address', read_only=True)
    hospital_phone = serializers.CharField(source='hospital.phone', read_only=True)
    results = LabResultValueSerializer(many=True, required=False)

    class Meta:
        model = LabReport
        fields = ['id', 'test_name', 'hospital_name', 'hospital_address', 'hospital_phone', 'date', 'status', 'results']

    def update(self, instance, validated_data):
        results_data = validated_data.pop('results', [])
        
        # Update LabReport fields
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Handle nested LabResultValue updates
        existing_result_ids = {result.id for result in instance.results.all()}
        updated_result_ids = {item.get('id') for item in results_data if item.get('id') is not None}
        
        # Delete results not in the update data
        results_to_delete = existing_result_ids - updated_result_ids
        LabResultValue.objects.filter(id__in=results_to_delete).delete()
        
        # Create or update results
        for item in results_data:
            result_id = item.get('id')
            if result_id:
                # Update existing result
                LabResultValue.objects.filter(id=result_id, report=instance).update(**item)
            else:
                # Create a new result
                LabResultValue.objects.create(report=instance, **item)
        
        return instance