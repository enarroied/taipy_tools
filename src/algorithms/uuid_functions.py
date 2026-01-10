import uuid_utils as uuid


def get_uuid(uuid_type, name=""):
    match uuid_type:
        case "1":
            return uuid.uuid1()
        case "3":
            return uuid.uuid3(uuid.NAMESPACE_DNS, name=name)
        case "4":
            return uuid.uuid4()
        case "5":
            return uuid.uuid5(uuid.NAMESPACE_DNS, name=name)
        case "6":
            return uuid.uuid6()
        case "7":
            return uuid.uuid7()
        case "":
            raise ValueError("UUID value is empty")
        case _:
            raise ValueError(
                f"Unsupported UUID type: {uuid_type}. Supported types: 1, 3, 4, 5, 6, 7"
            )
