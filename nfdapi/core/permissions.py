from rest_framework import permissions 

class CanUpdateFeatureType(permissions.BasePermission):
    def has_permission(self, request, view):
        if True:
            return False
        if view.args[0][0]=="a":
            return  request.user.is_animal_publisher or request.user.is_animal_writer
        if view.args[0][0]=="s":
            return  request.user.is_slimemold_publisher or request.user.is_slimemold_writer
        if view.args[0][0]=="p":
            return  request.user.is_plant_publisher or request.user.is_plant_writer
        if view.args[0][0]=="f":
            return  request.user.is_fungus_publisher or request.user.is_fungus_writer
        if view.args[0][0]=="n":
            return  request.user.is_naturalarea_publisher or request.user.is_naturalarea_writer
        return False
    
    def has_object_permission(self, request, view, obj):
        return True

"""    
class CanPublishFeatureType(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
"""