from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Relay(models.Model):
    name = models.CharField(max_length=100)
    mac_addr = models.CharField(max_length=12)
    state = models.BooleanField()
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='relays')

    def __str__(self) -> str:
        return f'Name: {self.name} / Mac: {self.mac_addr} / On: {self.state}'

    class Meta:
        db_table = 'relays'

class DH11(models.Model):
    name = models.CharField(max_length=100)
    mac_addr = models.CharField(max_length=12)
    temp = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='dh11s')

    def __str__(self) -> str:
        return f'Name: {self.name} / Mac: {self.mac_addr}'

    class Meta:
        db_table = 'dh11s'

