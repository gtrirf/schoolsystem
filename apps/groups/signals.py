from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.accounts.models import User, RoleCodes
from apps.groups.models import Group


@receiver(m2m_changed, sender=Group.students.through)
def update_user_role(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        for pk in pk_set:
            user = User.objects.get(pk=pk)
            if user.role != RoleCodes.objects.get(code='STUDENT').code:
                user.role = RoleCodes.objects.get(code='STUDENT').code
                user.save()

    elif action == "post_remove":
        for pk in pk_set:
            user = User.objects.get(pk=pk)
            if not Group.objects.filter(students=user).exists():
                user.role = RoleCodes.objects.get(code='GUEST').code
                user.save()
