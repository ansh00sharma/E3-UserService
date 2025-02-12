from rest_framework import serializers
from users.models import Service

class GetServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['uuid']

    def validate_uuid(self, value):
        if not value:
            raise serializers.ValidationError("Category Uuid is Required.")
        return value
    
    
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        ordering = ["name"]