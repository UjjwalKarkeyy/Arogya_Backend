from rest_framework import serializers
from .models import Doctor, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'description']


class DoctorSerializer(serializers.ModelSerializer):
    # keep PK write path
    specialty = serializers.PrimaryKeyRelatedField(queryset=Specialty.objects.all())
    # convenient read-only name
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    # optional richer read-only detail (handy in lists)
    specialty_detail = SpecialtySerializer(source='specialty', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name',
            'specialty', 'specialty_name', 'specialty_detail',
            'price', 'phone', 'email', 'address', 'hospital', 'opd_time',
            'qualifications', 'languages', 'bio', 'experience_years',
            'rating', 'is_available', 'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
        }

    # Guard rails for a couple of numeric fields
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be ≥ 0.")
        return value

    def validate_rating(self, value):
        # Your model allows up to 9.99; if you intend 0–5, enforce it here.
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value
