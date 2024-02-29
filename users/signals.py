from django.contrib.auth.models import Permission
from django.db.models import signals
from django.dispatch import receiver
from .models import User


@receiver(signals.m2m_changed, sender=User)
def add_permission(sender, instance, action, **kwargs):
    if instance.groups and action == 'post_add':
        for group in instance.groups.all():
            print(group)
            for group_permission in group.permissions.all():
                instance.user_permissions.add(group_permission)

    # instance.save()
