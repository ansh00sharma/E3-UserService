from rest_framework import serializers
from users.models import ServiceCategory

class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'  # This will include all fields
        ordering = ["name"]