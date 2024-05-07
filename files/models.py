from customers.models import Customer
from django.db import models
from django.utils import timezone

import os

def file_upload_path(instance, filename):
    customer_name = instance.customer.company_name
    year = instance.file_uploaded_at.year
    return os.path.join(filename, str(year), customer_name)


class File(models.Model):
    file_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_description = models.TextField(blank=False, null=False)
    file_path = models.FileField(upload_to=file_upload_path)
    file_uploaded_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.company_registered_at = timezone.now()
        self.company_last_edition = timezone.now()
        return super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name}"
    