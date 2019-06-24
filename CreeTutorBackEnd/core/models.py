from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from login.models import ModifiedUser


class Profile(models.Model):
    user = models.OneToOneField(ModifiedUser, on_delete=models.CASCADE)
    fav_colour = models.CharField(max_length=30, blank=True)
    # add profile fields here

# signal that creates a Profile. Triggered when a User is saved.
@receiver(post_save, sender=ModifiedUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# signal that saves a Profile. Triggered when a User is saved.
@receiver(post_save, sender=ModifiedUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()