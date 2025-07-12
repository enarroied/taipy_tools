import uuid_utils as uuid


def get_uuid(uuid_type, name=""):
    if uuid_type == "1":
        return uuid.uuid1()
    elif uuid_type == "3":
        return uuid.uuid3(uuid.NAMESPACE_DNS, name=name)
    elif uuid_type == "4":
        return uuid.uuid4()
    elif uuid_type == "5":
        return uuid.uuid5(uuid.NAMESPACE_DNS, name=name)
    elif uuid_type == "6":
        return uuid.uuid6()
    elif uuid_type == "7":
        return uuid.uuid7()
