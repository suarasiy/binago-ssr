# from django.dispatch import receiver
# from django.core.signals import request_finished
# from django.db.models.signals import pre_save

# from .models import Associations, AssociationsApprovalRequest


# @receiver(pre_save,  sender=Associations)
# def create_association(sender, instance, *args, **kwargs) -> None:
#     if not instance.approval:
#         approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.create()
#         instance.approval = approval
#         return
#     approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=instance.approval.id)
#     approval.save()
