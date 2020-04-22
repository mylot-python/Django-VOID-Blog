from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.ExSearch import WriteSearchV2
from utils.send_email import to_visitor
from .models import Article, Comments


@receiver(post_save, sender=Article)
def search_write_json(sender, instance=None, created=False, **kwargs):
    if created:
        WriteSearchV2(instance)

@receiver(post_save, sender=Comments)
def send_email(sender, instance=None, created=False, **kwargs):
    parent = instance.parent
    if parent and parent.re_mail == True:
        to_visitor(instance)

