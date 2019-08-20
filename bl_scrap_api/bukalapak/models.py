from django.db import models
from core.models import base_mod

# Create your models here.

class hasil(base_mod):
	kondisi = models.CharField(max_length = 25)
	produk = models.CharField(max_length = 255)
	harga = models.BigIntegerField()
	pelapak = models.CharField(max_length = 255)
	feedback = models.CharField(max_length = 255)
	link = models.CharField(max_length = 500)
