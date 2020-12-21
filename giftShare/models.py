from django.db import models

class GLUser(models.Model):
  username = models.CharField(max_length=40, unique=True, error_messages={
    "unique": "Username Already Used"
  })
  email = models.EmailField(max_length=254, unique=True, error_messages={
    "unique": "Email Already Used"
  })
  password = models.CharField(max_length=40)
  firstName = models.CharField(max_length=40)
  lastName = models.CharField(max_length=40)
  def __str__(self):
    return self.username

class Gift(models.Model):
  user = models.ForeignKey(GLUser, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
