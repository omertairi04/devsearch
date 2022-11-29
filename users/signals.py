# signals
from django.db.models.signals import post_save , post_delete
# signals with decorators
from django.dispatch import receiver

#email
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile
from django.contrib.auth.models import User

# signals post_save
# me decorator
#@receiver(post_save , sender=Profile)
def createProfile(sender , instance , created , **kwargs):
    if created:
        user = instance 
        profile = Profile.objects.create(
            user=user, 
            username = user.username , 
            email=user.email,
            name=user.first_name,
        )
        # email
        subject = 'Welcome to DevSearch'
        message = 'We are glad you joined us!'

        send_mail(
            subject ,
            message ,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

post_save.connect(createProfile , sender=User )

def updateUser(sender , instance , created , **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(updateUser , sender=Profile)
# me decorator
#@receiver(post_delete , sender=Profile)
def deleteUser(sender , instance, **kwargs):
    user = instance.user
    user.delete()

post_delete.connect(deleteUser , sender=Profile)


