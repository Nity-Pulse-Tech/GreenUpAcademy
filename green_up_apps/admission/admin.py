from django.contrib import admin
from .models import (
    Campus,
    Program,
    AdmissionSeason,
    EUAdmissionApplication,
    NonEUAdmissionApplication,
)

# ----------------- CAMPUS -----------------
@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# ----------------- PROGRAM -----------------
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "tuition_fee", "is_work_study",)
    list_filter = ("level", "is_work_study", "campuses")
    search_fields = ("name",)
    filter_horizontal = ("campuses",)


# ----------------- ADMISSION SEASON -----------------
@admin.register(AdmissionSeason)
class AdmissionSeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "academic_year", "start_date", "end_date", "is_active")
    list_filter = ("academic_year", "is_active")
    search_fields = ("name", "academic_year")
    ordering = ("-start_date",)


# ----------------- NON-EU APPLICATION -----------------
@admin.register(NonEUAdmissionApplication)
class NonEUAdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "nationality",
        "program",
        "campus",
        "season",
        "status",
        "application_date",
    )
    list_filter = ("status", "program", "campus", "season", "nationality")
    search_fields = ("first_name", "last_name", "email", "passport_number")
    readonly_fields = ("application_date",)


# ----------------- EU APPLICATION -----------------
@admin.register(EUAdmissionApplication)
class EUAdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "program",
        "campus",
        "season",
        "status",
        "application_date",
    )
    list_filter = ("status", "program", "campus", "season")
    search_fields = ("first_name", "last_name", "email", "institution")
    readonly_fields = ("application_date",)
