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
        
class User(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=50)
        lastname = models.CharField(max_length=50)
        password = models.CharField(max_length=50)
        email = models.EmailField()
        phone = models.BigIntegerField()
        created_at= models.DateTimeField(auto_now_add=True)
        updated_at= models.DateTimeField(auto_now=True)
        

        class Meta:
            db_table = 'user'
            ordering=['-created_at']