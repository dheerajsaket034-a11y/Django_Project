from django.db import models


class Prediction(models.Model):
    age = models.IntegerField()
    job = models.CharField(max_length=30)
    education = models.CharField(max_length=20)
    balance = models.IntegerField()
    housing = models.CharField(max_length=3)
    loan = models.CharField(max_length=3)
    contact = models.CharField(max_length=20)
    campaign = models.IntegerField()
    pdays = models.IntegerField()
    previous = models.IntegerField()
    poutcome = models.CharField(max_length=20)
    probability = models.FloatField()
    will_subscribe = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
