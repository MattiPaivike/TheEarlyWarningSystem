from rest_framework import serializers
from .models import Version, Software

class SoftwareSerializer(serializers.ModelSerializer):
    software = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Version
        fields = ('software', 'version')
