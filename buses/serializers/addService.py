from rest_framework import serializers
from users.models import Service

class AddServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name','description','category','price']

    def create(self, validated_data):
        """Create and return a new Service instance."""
        return Service.objects.create(**validated_data)
