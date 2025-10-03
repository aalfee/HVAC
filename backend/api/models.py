from django.db import models

class SimulationResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.JSONField()

class FaultPrediction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    prediction = models.JSONField()
