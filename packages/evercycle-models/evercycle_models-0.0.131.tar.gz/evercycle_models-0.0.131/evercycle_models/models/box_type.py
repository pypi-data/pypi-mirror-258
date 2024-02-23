from django.db import models
from .processor import Processor


class BoxType(models.Model):
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=150)
    updated_by = models.CharField(max_length=150, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    dimension = models.TextField(blank=True, null=True)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=1)

    class Meta:
        db_table = 'box_type'
