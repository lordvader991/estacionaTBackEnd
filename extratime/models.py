from django.db import models
class ExtraTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'extratime'
        ordering=['-created_at']