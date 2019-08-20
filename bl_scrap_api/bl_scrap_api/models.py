from django.db import models
from django.contrib.auth.models import User

class base_mod(models.Model):
	create_at = models.DateTimeField(auto_now_add = True)
	create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_created_by")
	modified_at  = models.DateTimeField(auto_now = True)
	modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_created_by")
	
	class Meta:
		abstact = True