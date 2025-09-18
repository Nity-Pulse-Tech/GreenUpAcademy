import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from green_up_apps.users.models import GreenUpBaseModel, Profile, User
from django.core.exceptions import ValidationError
from django.utils import timezone
from green_up_apps.global_data.enums import (
    CivilityChoices,
    ProgramLevelChoices,
    ApplicationStatusChoices,
    ApprenticeshipChoices,
)


# ----------------- CAMPUS -----------------
class Campus(GreenUpBaseModel):
    """
    Name: Campus
    Description: Model to store available campuses for the admission process.
    Author: ayemeleelgol@gmail.com
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Name of the campus (e.g., Paris, Reims).")
    )

    class Meta:
        verbose_name = _("Campus")
        verbose_name_plural = _("Campuses")

    def __str__(self):
        return self.name


# ----------------- PROGRAM -----------------
class Program(GreenUpBaseModel):
    """
    Name: Program
    Description: Model to store available programs for the admission process.
    Author: ayemeleelgol@gmail.com
    """
    name = models.CharField(
        max_length=200,
        help_text=_("Name of the program (e.g., BACHELOR Chef de Projet Performance Energétique).")
    )
    level = models.CharField(
        max_length=50,
        choices=ProgramLevelChoices.choices,
        help_text=_("Level of the program (Bachelor or Master).")
    )
    campuses = models.ManyToManyField(
        Campus,
        related_name='programs',
        help_text=_("Campuses where this program is offered.")
    )
    tuition_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Tuition fee for the program in EUR.")
    )
    is_work_study = models.BooleanField(
        default=False,
        help_text=_("Indicates if the program is offered as a work-study contract.")
    )

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")

    def __str__(self):
        return f"{self.name} ({self.level})"
    
# ----------------- DIPLOMA -----------------
class Diploma(GreenUpBaseModel):
    """
    Name: Diploma
    Description: Model to store diploma information for a user.
    Author: fotsoeddysteve@gmail.com
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diplomas',
        help_text=_("User who obtained or is pursuing this diploma.")
    )
    name = models.CharField(
        max_length=200,
        help_text=_("Name of the diploma obtained or in progress, including mention if applicable.")
    )
    institution = models.CharField(
        max_length=200,
        help_text=_("Institution where the diploma was obtained or is in progress.")
    )
    city_country = models.CharField(
        max_length=200,
        help_text=_("City and country of the institution.")
    )
    year = models.CharField(
        max_length=4,
        help_text=_("Year the diploma was obtained or expected.")
    )

    class Meta:
        verbose_name = _("Diploma")
        verbose_name_plural = _("Diplomas")

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name} ({self.year})"


# ----------------- ADMISSION SEASON -----------------
class AdmissionSeason(GreenUpBaseModel):
    """
    Name: AdmissionSeason
    Description: Defines admission seasons with their application start and end dates.
    Author: ayemeleelgol@gmail.com
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Name of the season (e.g., October 2025, February 2026).")
    )
    academic_year = models.CharField(
        max_length=20,
        help_text=_("Academic year for the season (e.g., 2025/2026).")
    )
    start_date = models.DateField(help_text=_("Start date for applications."))
    end_date = models.DateField(help_text=_("End date for applications."))
    session_start_date = models.DateField(help_text=_("Start date of the academic session (e.g., 15 October 2025)."))
    is_active = models.BooleanField(
        default=True,
        help_text=_("Whether this season is currently active.")
    )

    class Meta:
        verbose_name = _("Admission Season")
        verbose_name_plural = _("Admission Seasons")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

    def is_open(self):
        """Check if applications are currently open for this season."""
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date


# ----------------- BASE APPLICATION -----------------
class AdmissionApplication(GreenUpBaseModel):
    """
    Name: AdmissionApplication
    Description: Base model for admission applications, shared by EU and non-EU applicants.
    Author: ayemeleelgol@gmail.com
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_admission_applications",
        help_text=_("User submitting the application.")
    )
    season = models.ForeignKey(
        AdmissionSeason,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_applications",
        help_text=_("Admission season for this application.")
    )
    civility = models.CharField(
        max_length=10,
        choices=CivilityChoices.choices,
        blank=True,
        help_text=_("Civility of the applicant (Mr/Mrs).")
    )
    date_of_birth = models.DateField(help_text=_("Date of birth of the applicant."))
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_applications",
        help_text=_("Selected program for the application.")
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_applications",
        help_text=_("Selected campus for the application.")
    )
    diplomas = models.ManyToManyField(
        Diploma,
        related_name="%(class)s_applications",
        help_text=_("Diplomas associated with this application.")
    )

    # File fields with validators
    cv = models.FileField(
        upload_to='admission_documents/cv/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded CV (PDF/JPEG).")
    )
    motivation_letter = models.FileField(
        upload_to='admission_documents/motivation_letter/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded motivation letter (PDF/JPEG).")
    )
    portfolio = models.FileField(
        upload_to='admission_documents/portfolio/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        help_text=_("Uploaded portfolio (PDF/JPEG, optional).")
    )
    identity_document = models.FileField(
        upload_to='admission_documents/identity/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded identity document (PDF/JPEG).")
    )
    photo = models.ImageField(
        upload_to='admission_documents/photos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded identity photo (JPEG/PNG).")
    )
    academic_records = models.FileField(
        upload_to='admission_documents/academic_records/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded academic records or transcripts (PDF/JPEG).")
    )

    declaration_accepted = models.BooleanField(default=False, help_text=_("Indicates if the applicant has accepted the declaration."))
    how_heard = models.JSONField(default=dict, blank=True, help_text=_("Stores how the applicant heard about Green Up Academy (e.g., Internet, Word of Mouth)."))
    application_date = models.DateTimeField(default=timezone.now, help_text=_("Date and time when the application was submitted."))
    status = models.CharField(
        max_length=50,
        choices=ApplicationStatusChoices.choices,
        default=ApplicationStatusChoices.PENDING,
        help_text=_("Status of the application.")
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.get_full_name} - {self.program or 'No program'}"

    def clean(self):
        """Ensure application season is valid and user/profile data is present."""
        super().clean()
        if self.season and not self.season.is_open():
            raise ValidationError({"season": _("This admission season is closed. Please select an open season.")})
        if not self.user.first_name or not self.user.last_name or not self.user.email:
            raise ValidationError(_("User must have first name, last name, and email before submitting an application."))
        if not hasattr(self.user, 'profile') or not self.user.profile.phone_number or not self.user.profile.address or not self.user.profile.zip_code or not self.user.profile.city or not self.user.profile.country:
            raise ValidationError(_("User profile must have phone number, address, zip code, city, and country before submitting an application."))

    def update_user_and_profile(self, form_data):
        """Update User and Profile with form data if not already set."""
        self.user.first_name = form_data.get('first_name', self.user.first_name)
        self.user.last_name = form_data.get('last_name', self.user.last_name)
        self.user.email = form_data.get('email', self.user.email)
        self.user.save()

        profile, created = Profile.objects.get_or_create(user=self.user)
        profile.phone_number = form_data.get('phone_number', profile.phone_number)
        profile.address = form_data.get('address', profile.address)
        profile.zip_code = form_data.get('zip_code', profile.zip_code)
        profile.city = form_data.get('city', profile.city)
        profile.country = form_data.get('country', profile.country)
        profile.save()

# ----------------- NON-EU APPLICATION -----------------
class NonEUAdmissionApplication(AdmissionApplication):
    """
    Name: NonEUAdmissionApplication
    Description: Model for non-EU resident admission applications.
    Author: ayemeleelgol@gmail.com
    """
    place_of_birth = models.CharField(max_length=100, help_text=_("Place of birth of the applicant."))
    nationality = models.CharField(max_length=100, help_text=_("Nationality of the applicant."))
    passport_number = models.CharField(max_length=50, help_text=_("Passport number of the applicant."))
    level_of_studies = models.CharField(max_length=100, help_text=_("Level of studies of the applicant (e.g., Bachelor, Master)."))

    # Parent info (optional)
    parent_last_name = models.CharField(max_length=150, blank=True, null=True, help_text=_("Last name of the parent or guardian."))
    parent_first_name = models.CharField(max_length=150, blank=True, null=True, help_text=_("First name of the parent or guardian."))
    parent_phone_number = PhoneNumberField(blank=True, null=True, help_text=_("Phone number of the parent or guardian."))
    parent_email = models.EmailField(blank=True, null=True, help_text=_("Email address of the parent or guardian."))
    parent_address = models.TextField(blank=True, null=True, help_text=_("Address of the parent or guardian."))
    parent_postal_code = models.CharField(max_length=20, blank=True, null=True, help_text=_("Postal code of the parent's address."))
    parent_city = models.CharField(max_length=100, blank=True, null=True, help_text=_("City of the parent's address."))
    parent_country = models.CharField(max_length=100, blank=True, null=True, help_text=_("Country of the parent's address."))

    language_certificate = models.FileField(
        upload_to='admission_documents/language_certificates/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        help_text=_("Uploaded language proficiency certificate (PDF/JPEG, for non-francophones).")
    )

    class Meta:
        verbose_name = _("Non-EU Admission Application")
        verbose_name_plural = _("Non-EU Admission Applications")
        
# ----------------- EU APPLICATION -----------------
class EUAdmissionApplication(AdmissionApplication):
    """
    Name: EUAdmissionApplication
    Description: Model for EU resident admission applications.
    Author: ayemeleelgol@gmail.com
    """
    last_diploma = models.CharField(max_length=200, help_text=_("Last diploma obtained or in progress."))
    institution = models.CharField(max_length=200, help_text=_("Institution where the last diploma was obtained."))
    institution_city_country = models.CharField(max_length=200, help_text=_("City and country of the institution."))
    year_obtained = models.CharField(max_length=4, help_text=_("Year the diploma was obtained or expected."))
    apprenticeship_status = models.CharField(
        max_length=20,
        choices=ApprenticeshipChoices.choices,
        default=ApprenticeshipChoices.UNDECIDED,
        help_text=_("Status of apprenticeship for the program.")
    )
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1200.00, help_text=_("Registration fee in EUR, refundable under certain conditions."))
    declaration_place = models.CharField(max_length=100, help_text=_("Place where the declaration was signed."))
    declaration_date = models.DateField(help_text=_("Date when the declaration was signed."))
    signature = models.FileField(
        upload_to='admission_documents/signatures/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        null=True,
        help_text=_("Uploaded handwritten or digital signature (PDF/JPEG).")
    )

    class Meta:
        verbose_name = _("EU Admission Application")
        verbose_name_plural = _("EU Admission Applications")

    def clean(self):
        """Validate registration fee and season rules."""
        super().clean()
        if self.registration_fee < 0:
            raise ValidationError({"registration_fee": _("Registration fee cannot be negative.")})
