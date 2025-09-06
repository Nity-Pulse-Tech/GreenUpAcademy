from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    User,
    Profile,
    Partners,
    ContactUs,
    CompanySettings,
)


class UserAdmin(BaseUserAdmin):
    """Custom admin panel for User model"""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("fullname", "first_name", "last_name", "profile_picture")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_admin", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Other"), {"fields": ("ip_address", "has_accepted_terms", "is_manually_deleted")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "fullname", "is_staff", "is_superuser", "is_admin", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_admin", "is_active")
    search_fields = ("email", "fullname", "first_name", "last_name")
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "city", "phone_number")
    search_fields = ("user__email", "country", "city", "phone_number")


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active",)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "is_resolved", "created")
    list_filter = ("is_read", "is_resolved")
    search_fields = ("name", "email", "subject")
    ordering = ("-created",)


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ("company_name", "primary_email", "phone_number", "is_active", "timezone")
    search_fields = ("company_name", "primary_email", "phone_number")
    list_filter = ("is_active", "timezone")
    ordering = ("-is_active", "company_name")


# Register custom User separately since it overrides Django’s User
admin.site.register(User, UserAdmin)
