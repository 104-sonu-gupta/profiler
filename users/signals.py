from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import userProfile


@receiver(post_save, sender = User)                  # decorator way
def createProfile(sender, instance, created, **kwargs):
    # print('Users update event Triggered')
    if created:
        user = instance
        userProfile.objects.create(
            user = user, 
            username = user.username,                    # this is not working rn b/c user creation form is 2 step
            name = user.first_name +' '+ user.last_name, # this will work now b/c we created CustomRegistrationForm
            email = user.email,                          
        )

        
def deleteUser(sender, instance, **kwargs):     # deleting user when user deleted from admin userProfile
    user = instance.user                        # because user will still be left out in Users table
    user.delete()

post_delete.connect(deleteUser, sender = userProfile)       # simple way 