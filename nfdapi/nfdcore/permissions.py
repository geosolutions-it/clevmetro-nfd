from rest_framework import permissions 
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.permissions import SAFE_METHODS


def get_permissions(user, featuretype_name):
    """
    Gets the permissions for the provided user and feature type.
    Returns a tuple (can_write, can_publish)
    """
    if user.is_superuser:
        result = (True, True)
    else:
        is_writer = getattr(
            user, "is_{}_writer".format(featuretype_name), False)
        is_publisher = getattr(
            user, "is_{}_publisher".format(featuretype_name), False)
        result = (is_writer, is_publisher)
    return result


def can_publish_feature_type(user, featuretype_name):
    if featuretype_name[0]=="a":
        return user.is_animal_publisher
    if featuretype_name[0]=="s":
        return user.is_slimemold_publisher
    if featuretype_name[0]=="p":
        return user.is_plant_publisher
    if featuretype_name[0]=="f":
        return user.is_fungus_publisher
    if featuretype_name[0]=="n":
        return user.is_naturalarea_publisher
    return False


def can_update_feature_type(user, featuretype_name):
    is_publisher = getattr(user, "is_{}_publisher".format(
        featuretype_name), False)
    return is_publisher or getattr(
        user, "is_{}_writer".format(featuretype_name), False)


class CanWriteOrUpdateAny(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        else:
            return (
                request.user.is_animal_publisher or
                request.user.is_animal_writer or
                request.user.is_slimemold_publisher or
                request.user.is_slimemold_writer or
                request.user.is_plant_publisher or
                request.user.is_plant_writer or
                request.user.is_fungus_publisher or
                request.user.is_fungus_writer or
                request.user.is_naturalarea_publisher or
                request.user.is_naturalarea_writer
            )

    def has_object_permission(self, request, view, obj):
        return True

    
class CanUpdateFeatureType(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.method not in SAFE_METHODS and not user.is_superuser:
            return can_update_feature_type(request.user, view.args[0])
        return True
    
    def has_object_permission(self, request, view, obj):
        return True


class CanCreateFeatureType(permissions.BasePermission):
    FEATURETYPE_NAME = ""

    def has_permission(self, request, view):
        result = True
        user = request.user
        if request.method == 'POST' and not user.is_superuser:
            feature_type_name = view.args[0]
            result = getattr(
                user,
                "is_{}_writer".format(self.FEATURETYPE_NAME),
                False
            )
        return result
    
    def has_object_permission(self, request, view, obj):
        return True


class CanCreateAnimals(CanCreateFeatureType):
    FEATURETYPE_NAME = "animal"


class CanCreatePlants(CanCreateFeatureType):
    FEATURETYPE_NAME = "plant"


class CanCreateFungus(CanCreateFeatureType):
    FEATURETYPE_NAME = "fungus"


class CanCreateSlimeMold(CanCreateFeatureType):
    FEATURETYPE_NAME = "slimemold"


class CanCreateNaturalAreas(CanCreateFeatureType):
    FEATURETYPE_NAME = "naturalarea"
