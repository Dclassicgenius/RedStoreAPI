# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver

# from .models import Account, UserProfile


# @receiver(post_save, sender=Account)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.profile.save()