from rest_framework import serializers
from .models import Version, Software
from collections import OrderedDict

class SoftwareSerializer(serializers.ModelSerializer):
    software = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Version
        fields = ('software', 'version', 'dllink', 'dllink_x86', 'dllink_x64', 'checksum', 'checksum_x86', 'checksum_x64','checksum_type')

    def to_representation(self, instance):
        result = super(SoftwareSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not ""])
