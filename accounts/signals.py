from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Account,UserProfile

#Django signal qui permet d'enregister un evement avant ou apres execution d'une action

@receiver(post_save, sender=Account)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
        print(created)
        if created:
             UserProfile.objects.create(user=instance)
             print('user profile is created')
        else:
            try:
                profile = UserProfile.objects.get(user=instance)
                profile.save()
            except:
                #create the userprofile if not exst
                UserProfile.objects.create(user=instance)
                print('Profile was not exist, but one has been created')
            print('user is updated')



@receiver(pre_save, sender=Account)
def pre_save_profile_receiver(sender, instance, **kwargs):
     print(instance.username, 'this user is being saved')