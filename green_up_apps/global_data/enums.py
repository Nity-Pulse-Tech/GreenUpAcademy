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
    
class EntryLevelChoices(models.TextChoices):
    BAC = "BAC", _("BAC")
    BAC_PLUS_2 = "BAC+2", _("BAC +2")
    BAC_PLUS_3 = "BAC+3", _("BAC +3")
    BAC_PLUS_4 = "BAC+4", _("BAC +4")
    BAC_PLUS_5 = "BAC+5", _("BAC +5")