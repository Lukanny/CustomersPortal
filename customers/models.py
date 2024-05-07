from django.db import models
from django.utils import timezone

class Customer(models.Model):
    company_worker_name = models.CharField(max_length=254)
    company_worker_id = models.CharField(max_length=9)
    company_worker_nif = models.CharField(max_length=11)
    company_worker_position = models.CharField(max_length=254)
    company_name = models.CharField(max_length=254)
    company_address = models.CharField(max_length=254)
    company_number = models.CharField(max_length=15)
    company_email = models.EmailField(max_length=254)
    company_registered_at = models.DateTimeField(editable=False)
    company_last_edition = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.company_registered_at = timezone.now()
        self.company_last_edition = timezone.now()
        return super(Customer, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.company_name}"
    

