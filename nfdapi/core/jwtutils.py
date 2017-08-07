

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': {
            'name': user.username,
            'is_staff': user.is_staff,
            'plant_writer': user.is_plant_writer,
            'plant_publisher': user.is_plant_publisher,
            'animal_writer': user.is_animal_writer,
            'animal_publisher': user.is_animal_publisher,
            'slimemold_writer': user.is_slimemold_writer,
            'slimemold_publisher': user.is_slimemold_publisher,
            'fungus_writer': user.is_fungus_writer,
            'fungus_publisher': user.is_fungus_publisher,
            'naturalarea_writer': user.is_naturalarea_writer,
            'naturalarea_publisher': user.is_naturalarea_publisher
            }
    }