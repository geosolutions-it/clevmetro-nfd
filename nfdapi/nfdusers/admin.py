from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_plant_writer",
        "is_plant_publisher",
        "is_animal_writer",
        "is_animal_publisher",
        "is_slimemold_writer",
        "is_slimemold_publisher",
        "is_fungus_writer",
        "is_fungus_publisher",
        "is_naturalarea_writer",
        "is_naturalarea_publisher",
    )
    list_editable = (
        "is_plant_writer",
        "is_plant_publisher",
        "is_animal_writer",
        "is_animal_publisher",
        "is_slimemold_writer",
        "is_slimemold_publisher",
        "is_fungus_writer",
        "is_fungus_publisher",
        "is_naturalarea_writer",
        "is_naturalarea_publisher",
    )
