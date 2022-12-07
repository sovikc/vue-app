import uuid


def get_uuid() -> str:
    random_uuid = uuid.uuid4()
    uuid_hex = random_uuid.hex
    return uuid_hex
