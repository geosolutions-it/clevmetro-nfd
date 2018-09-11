

def jwt_response_payload_handler(token, user=None, request=None):
    result = {
        "token": token,
        "user": {
            "name": user.username,
            "is_staff": user.is_staff,
        },
    }
    feature_types = [
        "animal",
        "fungus",
        "naturalarea",
        "plant",
        "slimemold",
    ]
    for feature_type in feature_types:
        for role in ["writer", "publisher"]:
            permission_name = "{}_{}".format(feature_type, role)
            if user.is_superuser:
                permission_value = True
            else:
                permission_value = getattr(
                    user, "is_{}".format(permission_name), False)
            result["user"][permission_name] = permission_value
    return result
