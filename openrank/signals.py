from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=RatingListStage)
def update_pairings_finished(sender, instance, **kwargs):
    for pairing in instance.pairings.all():
        print ('Attemping update on', pairing)
        pairing.compute_finished()
        pairing.save(update_fields=['finished'])