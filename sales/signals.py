from django.db.models.signals import post_save
from django.dispatch import receiver
from sales.models import SalesLead, Telecaller


@receiver(post_save, sender=SalesLead)
def update_telecaller_on_sales_lead_save(sender, instance, created, **kwargs):
    """
    Updates the telecaller's max_leads when a new SalesLead is created.
    """
    if created: # Only increment max_leads if this is a new SalesLead instance
        instance.telecaller.max_leads += 1
        instance.telecaller.save()


@receiver(post_save, sender=Telecaller)
def initialize_telecaller_max_leads(sender, instance, created, **kwargs):
    """
    Ensures max_leads is set appropriately for new Telecallers with the "sales" role.
    """
    if created and instance.role == "sales":  # Only act on newly created Telecaller instances
        if instance.max_leads is None:  # Optional: Initialize max_leads if not already set
            instance.max_leads = 1
        else:
            instance.max_leads += 1
        instance.save()