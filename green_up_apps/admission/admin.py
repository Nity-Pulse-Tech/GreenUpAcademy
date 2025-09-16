from django.contrib import admin
from .models import Campus, Program, EUAdmissionApplication, NonEUAdmissionApplication

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
        "status",
        "application_date",
    )
    list_filter = ("status", "program", "campus", "nationality")
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
        "status",
        "application_date",
    )
    list_filter = ("status", "program", "campus")
    search_fields = ("first_name", "last_name", "email", "institution")
    readonly_fields = ("application_date",)
