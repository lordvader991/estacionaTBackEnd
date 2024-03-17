from django.db import models

class PersonModel(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.BigIntegerField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = 'person'
        ordering=['-created_at']
    
