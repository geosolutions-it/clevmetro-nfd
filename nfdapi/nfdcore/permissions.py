from rest_framework import permissions 
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.permissions import SAFE_METHODS

def get_permissions(user, featuretype_name):
    """
    Gets the permissions for the provided user and feature type.
    Returns a tuple (can_write, can_publish)
    """
    if featuretype_name[0]=="a":
        return (user.is_animal_writer, user.is_animal_publisher) 
    if featuretype_name[0]=="s":
        return (user.is_slimemold_writer, user.is_slimemold_publisher)
    if featuretype_name[0]=="p":
        return (user.is_plant_writer, user.is_plant_publisher)
    if featuretype_name[0]=="f":
        return (user.is_fungus_writer, user.is_fungus_publisher)
    if featuretype_name[0]=="n":
        return (user.is_naturalarea_writer, user.is_naturalarea_publisher)
    return (False, False)

def can_create_feature_type(user, featuretype_name):
    if featuretype_name[0]=="a":
        return user.is_animal_writer
    if featuretype_name[0]=="s":
        return user.is_slimemold_writer
    if featuretype_name[0]=="p":
        return user.is_plant_writer
    if featuretype_name[0]=="f":
        return user.is_fungus_writer
    if featuretype_name[0]=="n":
        return user.is_naturalarea_writer
    return False

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
    if featuretype_name[0]=="a":
        return user.is_animal_publisher or user.is_animal_writer
    if featuretype_name[0]=="s":
        return user.is_slimemold_publisher or user.is_slimemold_writer
    if featuretype_name[0]=="p":
        return user.is_plant_publisher or user.is_plant_writer
    if featuretype_name[0]=="f":
        return user.is_fungus_publisher or user.is_fungus_writer
    if featuretype_name[0]=="n":
        return user.is_naturalarea_publisher or user.is_naturalarea_writer
    return False

class CanWriteOrUpdateAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_animal_publisher or \
                request.user.is_animal_writer or \
                request.user.is_slimemold_publisher or \
                request.user.is_slimemold_writer or \
                request.user.is_plant_publisher or \
                request.user.is_plant_writer or \
                request.user.is_fungus_publisher or \
                request.user.is_fungus_writer or \
                request.user.is_naturalarea_publisher or \
                request.user.is_naturalarea_writer)
    def has_object_permission(self, request, view, obj):
        return True
    
class CanUpdateFeatureType(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return can_update_feature_type(request.user, view.args[0])
        return True
    
    def has_object_permission(self, request, view, obj):
        return True

class CanCreateFeatureType(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return can_create_feature_type(request.user, view.args[0])
        return True
    
    def has_object_permission(self, request, view, obj):
        return True

class CanCreateAnimals(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return request.user.is_animal_writer
        return True
    
class CanCreatePlants(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return request.user.is_plant_writer
        return True

class CanCreateFungus(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return request.user.is_fungus_writer
        return True

class CanCreateSlimeMold(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return request.user.is_slimemold_writer
        return True

class CanCreateNaturalAreas(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='POST':
            return request.user.is_naturalarea_writer
        return True
