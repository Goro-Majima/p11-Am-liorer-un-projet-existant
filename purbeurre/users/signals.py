"""Simultaneously create profile related to the creation of a user"""
from django.db.models.signals import post_save #after user is created
from django.contrib.auth.models import User #the sender sends the signal
from django.dispatch import receiver #function gets the signal and perform some tasks
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """ Create profile in database """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """ Save profile in database """
    instance.profile.save()
