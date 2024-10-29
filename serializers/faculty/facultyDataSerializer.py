from rest_framework import serializers
from faculty.models import Faculty


class FacultySerializer(serializers.Serializer):
    user_id = serializers.CharField()