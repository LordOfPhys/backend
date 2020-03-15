# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'user')
    killer = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'killer')
    email = models.EmailField(max_length = 100, default = 'Mail')
    name = models.CharField(max_length = 100, default = 'Name')
    x_location = models.CharField(max_length = 100, default = '0')
    y_location = models.CharField(max_length = 100, default = '0')
    status = models.CharField(max_length = 100, default = '0')
    alive = models.CharField(max_length = 100, default = '1')

    class Meta:
        db_table = 'user_profile'
    
    def get_alive(self):
        return self.alive

    def set_alive(self, alive):
        self.alive = alive
        self.save()
    
    def get_status(self):
        return self.status    
   
    def def_status(self, status):
        self.status = status
        self.save()
 
    def definition_killer(self, to_kill):
        self.killer = to_kill
        self.save()

    def get_killer(self):
        return self.killer

    def __unicode__(self):
        return self.user.username

    def set_x(self, x):
        self.x_location = x
        self.save()

    def set_y(self, y):
        self.y_location = y
        self.save()

    def get_x(self):
        return self.x_location
 
    def get_y(self):
        return self.y_location

