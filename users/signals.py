# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
# from users.models import User
# #User= settings.AUTH_USER_MODEL

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         print("Created")
#         Token.objects.create(user=instance)
#         print(token)
#     else:
#         print("error")