#!/usr/bin/env python
"""
Script to create sample data for Lab Result functionality
Run this after starting the Django server to populate test data
"""
import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arogya_Backend.settings')
django.setup()

from Lab_Result.models import LabTest, Hospital, LabReport, LabResultValue

def create_sample_data():
    print("Creating sample lab result data...")
    
    # Create sample lab tests
    lab_tests = [
        "Complete Blood Count (CBC)",
        "Lipid Profile",
        "Liver Function Test (LFT)",
        "Kidney Function Test (KFT)",
        "Thyroid Function Test (TFT)",
        "Blood Sugar Test",
        "Urine Analysis",
        "ECG",
    ]
    
    for test_name in lab_tests:
        test, created = LabTest.objects.get_or_create(name=test_name)
        if created:
            print(f"Created lab test: {test_name}")
    
    # Create sample hospitals
    hospitals_data = [
        {"name": "City Hospital", "type": "General", "address": "Kathmandu, Nepal", "phone": "+977-1-4444444"},
        {"name": "Medicare Center", "type": "Diagnostic", "address": "Lalitpur, Nepal", "phone": "+977-1-5555555"},
        {"name": "Health Care Clinic", "type": "Clinic", "address": "Bhaktapur, Nepal", "phone": "+977-1-6666666"},
        {"name": "National Medical Center", "type": "Specialized", "address": "Pokhara, Nepal", "phone": "+977-61-777777"},
    ]
    
    for hospital_data in hospitals_data:
        hospital, created = Hospital.objects.get_or_create(
            name=hospital_data["name"],
            defaults=hospital_data
        )
        if created:
            print(f"Created hospital: {hospital_data['name']}")
    
    # Create sample lab reports
    cbc_test = LabTest.objects.get(name="Complete Blood Count (CBC)")
    lipid_test = LabTest.objects.get(name="Lipid Profile")
    city_hospital = Hospital.objects.get(name="City Hospital")
    medicare_center = Hospital.objects.get(name="Medicare Center")
    
    # CBC Report
    cbc_report, created = LabReport.objects.get_or_create(
        patient_id="PAT001",
        test=cbc_test,
        hospital=city_hospital,
        defaults={
            "date": date.today(),
            "status": "Ready"
        }
    )
    
    if created:
        print("Created CBC report")
        # Add CBC result values
        cbc_results = [
            {"sub_test_name": "Hemoglobin", "value": "14.2", "unit": "g/dL", "reference_range": "12.0-15.5"},
            {"sub_test_name": "RBC Count", "value": "4.8", "unit": "million/μL", "reference_range": "4.2-5.4"},
            {"sub_test_name": "WBC Count", "value": "7200", "unit": "/μL", "reference_range": "4000-11000"},
            {"sub_test_name": "Platelet Count", "value": "280000", "unit": "/μL", "reference_range": "150000-450000"},
        ]
        
        for result_data in cbc_results:
            LabResultValue.objects.create(report=cbc_report, **result_data)
    
    # Lipid Profile Report
    lipid_report, created = LabReport.objects.get_or_create(
        patient_id="PAT001",
        test=lipid_test,
        hospital=medicare_center,
        defaults={
            "date": date.today(),
            "status": "Ready"
        }
    )
    
    if created:
        print("Created Lipid Profile report")
        # Add Lipid Profile result values
        lipid_results = [
            {"sub_test_name": "Total Cholesterol", "value": "180", "unit": "mg/dL", "reference_range": "<200"},
            {"sub_test_name": "HDL Cholesterol", "value": "45", "unit": "mg/dL", "reference_range": ">40"},
            {"sub_test_name": "LDL Cholesterol", "value": "110", "unit": "mg/dL", "reference_range": "<100"},
            {"sub_test_name": "Triglycerides", "value": "125", "unit": "mg/dL", "reference_range": "<150"},
        ]
        
        for result_data in lipid_results:
            LabResultValue.objects.create(report=lipid_report, **result_data)
    
    print("\nSample data creation completed!")
    print(f"Lab Tests: {LabTest.objects.count()}")
    print(f"Hospitals: {Hospital.objects.count()}")
    print(f"Lab Reports: {LabReport.objects.count()}")
    print(f"Result Values: {LabResultValue.objects.count()}")

if __name__ == "__main__":
    create_sample_data()
