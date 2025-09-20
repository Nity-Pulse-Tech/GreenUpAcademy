import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from green_up_apps.users.models import GreenUpBaseModel
from green_up_apps.admission.models import Program, Campus

class Formation(GreenUpBaseModel):
    """
    Name: Formation
    Description: Model to store academic formation details, linked to programs and campuses.
    Author: ayemeleelgol@gmail.com
    """
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        related_name='formations',
        help_text=_("Associated academic program from the admission module.")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text=_("URL-friendly identifier for the formation, auto-generated from program name.")
    )
    image = models.ImageField(
        upload_to='formations/images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])],
        null=True,
        blank=True,
        help_text=_("Image representing the formation (e.g., program banner).")
    )
    objectives = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of objectives for the formation (e.g., ['Atteindre un niveau de savoirs académiques...', 'Développer un niveau de formation...']).")
    )
    competencies = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of academic competencies targeted by the formation.")
    )
    domain = models.CharField(
        max_length=100,
        help_text=_("Academic domain of the formation (e.g., Sciences de gestion, Informatique).")
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Specialization within the domain, if applicable (e.g., Vente & Marketing).")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Indicates whether the formation is actively offered.")
    )
    learn_more_url = models.URLField(
        blank=True,
        null=True,
        help_text=_("URL for detailed information about the formation.")
    )

    class Meta:
        verbose_name = _("Formation")
        verbose_name_plural = _("Formations")
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_deleted']),
        ]
        ordering = ['program__name']

    def save(self, *args, **kwargs):
        if not self.slug and self.program:
            base_slug = slugify(self.program.name)
            slug = base_slug
            counter = 1
            while Formation.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.program.name if self.program else 'Unnamed Formation'} ({self.program.level if self.program else 'No Level'})"

    def clean(self):
        """Validate model data."""
        super().clean()

class FormationOption(GreenUpBaseModel):
    """
    Name: FormationOption
    Description: Model to store specific options within a formation (e.g., Systèmes d’information).
    Author: ayemeleelgol@gmail.com
    """
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='options',
        help_text=_("Parent formation for this option.")
    )
    name = models.CharField(
        max_length=100,
        help_text=_("Name of the option (e.g., Systèmes d’information, Programmation applications).")
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Description of the option.")
    )
    competencies = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Specific competencies targeted by this option.")
    )

    class Meta:
        verbose_name = _("Formation Option")
        verbose_name_plural = _("Formation Options")
        unique_together = ('formation', 'name')

    def __str__(self):
        return f"{self.name} - {self.formation.program.name if self.formation.program else 'Unnamed Formation'}"