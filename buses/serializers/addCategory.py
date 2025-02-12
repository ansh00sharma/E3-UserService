from rest_framework import serializers
from users.models import ServiceCategory

class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['name','description']

    def create(self, validated_data):
        """Create and return a new ServiceCategory instance."""
        return ServiceCategory.objects.create(**validated_data)
