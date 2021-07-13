from django.db import models
from accounts.models import CustomUser
import uuid

# Create your models here.

class Room(models.Model):

    code = models.CharField(max_length=6, primary_key=True, default=uuid.uuid4().hex[:6])
    room_pic = models.ImageField(upload_to ='room_pic')
    name = models.CharField(max_length=40)
    participants= models.ManyToManyField('accounts.CustomUser')

    def __str__(self):
        return self.name

class Message(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}-{self.message}"
    
    class Meta:
        ordering = ['-timestamp']