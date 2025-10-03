from rest_framework import serializers

class SimulationInputSerializer(serializers.Serializer):
    building_id = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    parameters = serializers.JSONField(required=False)

class PredictionInputSerializer(serializers.Serializer):
    sensor_data = serializers.JSONField()
    timestamp = serializers.DateTimeField()
