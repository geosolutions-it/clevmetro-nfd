from django.db import models
from django.contrib.auth import models as contrib_models

class User(contrib_models.AbstractUser):
    is_plant_writer = models.BooleanField(default=False)
    is_plant_publisher = models.BooleanField(default=False)
    is_animal_writer = models.BooleanField(default=False)
    is_animal_publisher = models.BooleanField(default=False)
    is_slimemold_writer = models.BooleanField(default=False)
    is_slimemold_publisher = models.BooleanField(default=False)
    is_fungus_writer = models.BooleanField(default=False)
    is_fungus_publisher = models.BooleanField(default=False)
    is_naturalarea_writer = models.BooleanField(default=False)
    is_naturalarea_publisher = models.BooleanField(default=False)
