from django.db import models
from .organization import Organization
from .processor import Processor


class BoxLogic(models.Model):
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=150)
    updated_by = models.CharField(max_length=150, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    box_configuration = models.TextField()

    class Meta:
        db_table = 'box_logic'
