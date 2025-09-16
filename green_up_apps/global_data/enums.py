from django.utils.translation import gettext_lazy as _
from django.db import models


class CivilityChoices(models.TextChoices):
    MR = "Mr", _("Mr")
    MRS = "Mrs", _("Mrs")


class ProgramLevelChoices(models.TextChoices):
    BACHELOR = "Bachelor", _("Bachelor")
    MASTER = "Master", _("Master")


class ApplicationStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    REVIEWED = "reviewed", _("Reviewed")
    ACCEPTED = "accepted", _("Accepted")
    REJECTED = "rejected", _("Rejected")


class ApprenticeshipChoices(models.TextChoices):
    YES = "yes", _("Yes")
    NO = "no", _("No")
    UNDECIDED = "undecided", _("Undecided")
