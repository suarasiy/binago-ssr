from django.db import models

from authentication.models import User
from Events.models import Events
from Associations.models import Associations


class UserNotification(models.Model):

    class NotificationType(models.TextChoices):
        INVOICE_CREATED = "INVOICE_CREATED", ("Invoice Created")
        INVOICE_SUCCESS = "INVOICE_SUCCESS", ("Invoice Success")
        INVOICE_FAILED = "INVOICE_FAILED", ("Invoice Failed")
        ASSOCIATION_CREATED = "ASSOCIATION_CREATED", ("Association Created")
        ASSOCIATION_APPROVAL_ACCEPTED = "ASSOCIATION_APPROVAL_ACCEPTED", ("Association Approval Accepted")
        ASSOCIATION_APPROVAL_REJECTED = "ASSOCIATION_APPROVAL_REJECTED", ("Association Approval Rejected")
        ASSOCIATION_INVITATION = "ASSOCIATION_INVITATION", ("Association Invitation")
        ASSOCIATION_INVITATION_ACCEPTED = "ASSOCIATION_INVITATION_ACCEPTED", ("Association Invitation Accepted")
        ASSOCIATION_INVITATION_REJECTED = "ASSOCIATION_INVITATION_REJECTED", ("Association Invitation Rejected")
        ASSOCIATION_PERMISSION_TO_MANAGER = "ASSOCIATION_PERMISSION_TO_MANAGER", ("Association Permission to Manager")
        ASSOCIATION_PERMISSION_TO_MEMBER = "ASSOCIATION_PERMISSION_TO_MEMBER", ("Association Permission to Member")
        ASSOCIATION_POSTED_NEW_EVENT = "ASSOCIATION_POSTED_NEW_EVENT", ("Association Posted New Event")
        EVENT_INVITATION = "EVENT_INVITATION", ("Event Invitation")
        EVENT_INVITATION_ACCEPTED = "EVENT_INVITATION_ACCEPTED", ("Event Invitation Accepted")
        EVENT_INVITATION_REJECTED = "EVENT_INVITATION_REJECTED", ("Event Invitation Rejected")
        EVENT_ENROLLED_SUCCESS = "EVENT_ENROLLED_SUCCESS", ("Event Enrolled Success")
        EVENT_ENROLLED_FAILED = "EVENT_ENROLLED_FAILED", ("Event Enrolled Failed")
        EVENT_POINT_RECEIVED = "EVENT_POINT_RECEIVED", ("Event Point Received")
        EVENT_CERTIFICATE_RECEIVED = "EVENT_CERTIFICATE_RECEIVED", ("Event Certificate Received")
        EVENT_REMINDER_BEFORE = "EVENT_REMINDER_BEFORE", ("Event Reminder Before")
        EVENT_REMINDER_STARTED = "EVENT_REMINDER_STARTED", ("Event Reminder Started")
        EVENT_REMINDER_ENDED = "EVENT_REMINDER_ENDED", ("Event Reminder Ended")
        EVENT_GOT_REVIEW = "EVENT_GOT_REVIEW", ("Event Got Review")
        EVENT_GOT_ATTENDED = "EVENT_GOT_ATTENDED", ("Event Got Attended")
        EVENT_GOT_REACTION = "EVENT_GOT_REACTION", ("Event Got Reaction")
        NEW_ACCOUNT_MESSAGE = "NEW_ACCOUNT_MESSAGE", ("New Account Message")

    # target user that retrieve notification
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField(choices=NotificationType.choices, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    # sender or user that triggered the notification that will be sended to the target
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sender")
    # individual codependent miscellaneous foreignkey
    event = models.ForeignKey(Events, on_delete=models.CASCADE, blank=True, null=True)
    association = models.ForeignKey(Associations, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.type

    class Meta:
        verbose_name_plural = 'User Notifications'


class UserNotificationAction(models.Model):

    class ActionType(models.TextChoices):
        ASSOCIATION_INVITATION_ACCEPT = "ASSOCIATION_INVITATION_ACCEPT", ("Association Invitation Accept")
        ASSOCIATION_INVITATION_REJECT = "ASSOCIATION_INVITATION_REJECT", ("Association Invitation Reject")
        ASSOCIATION_DETAIL = "ASSOCIATION_DETAIL", ("Association Detail")
        EVENT_INVITATION_ACCEPT = "EVENT_INVITATION_ACCEPT", ("Event Invitation Accept")
        EVENT_INVITATION_REJECT = "EVENT_INVITATION_REJECT", ("Event Invitation Reject")
        EVENT_STREAM_DETAIL = "EVENT_STREAM_DETAIL", ("Event Stream Detail")
        EVENT_DETAIL = "EVENT_DETAIL", ("Event Detail")
        INVOICE_DETAIL = "INVOICE_DETAIL", ("Invoice Detail")
        PROFILE_POINT_DETAIL = "PROFILE_POINT_DETAIL", ("Profile Point Detail")
        PROFILE_CERTIFICATE_DETAIL = "PROFILE_CERTIFICATE_DETAIL", ("Profile Certificate Detail")

    class ActionStyle(models.TextChoices):
        RED = "RED", ("Red")
        BLUE = "BLUE", ("Blue")
        GREEN = "GREEN", ("Green")
        YELLOW = "YELLOW", ("Yellow")
        SLATE = "SLATE", ("Slate")
        BLACK = "BLACK", ("Black")

    notification = models.ForeignKey(UserNotification, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    type = models.TextField(choices=ActionType.choices, db_index=True)
    style = models.TextField(choices=ActionStyle.choices)
    is_priority = models.BooleanField(default=None, blank=True, null=True)
    target_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.label

    class Meta:
        verbose_name_plural = "User Notifications Action"
