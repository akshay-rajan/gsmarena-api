from rest_framework import serializers

class BrandSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    devices = serializers.IntegerField()

class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    img = serializers.URLField()
    description = serializers.CharField(max_length=255)

class DeviceDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    img = serializers.URLField()
    quick_spec = serializers.ListField()
    detail_spec = serializers.ListField()
    pricing = serializers.ListField()
    popularity = serializers.FloatField()
