from tokenize import group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

#  على ش ان لما اعمل إنشاء حساب يضيف الحساب بقاعدة البيانات ويعمله بالقروب 

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance, 
            name = instance.username,
            )
post_save.connect(customer_profile, sender=User)