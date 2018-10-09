from django.db.models.signals import post_save, post_delete
from django.db.utils import OperationalError, ProgrammingError
from django.dispatch import receiver
from models import CRUDLog


def create_object(action, instance, sender):
    if sender == CRUDLog:
        return
    try:
        return CRUDLog.objects.create(
            action=action,
            model=instance._meta.object_name,
            app=instance._meta.app_label
        )
    except (OperationalError, ProgrammingError):
        return


@receiver(post_save)
def log_save_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return

    action = 'created' if created else 'updated'
    create_object(action, instance, sender)


@receiver(post_delete)
def log_delete_signal(sender, instance, **kwargs):
    create_object('deleted', instance, sender)
