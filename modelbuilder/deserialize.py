import json

from datetime import date, datetime
from dateutil.parser import parse

from modelbuilder.model import Model
from modelbuilder.exceptions import DeserializationException

MAPPING_TYPES = [dict]
SEQUENCE_TYPES = set((list, tuple))
DATETIME_TYPES = set((date, datetime))
PRIMITIVE_TYPES = set((int, str, bool, float))


def deserialize(obj_type, payload):
    """ Takes a dict payload and turns it into a class of type obj_type """
    if payload is None:
        return None

    try:
        payload = json.loads(payload)
    except TypeError:
        payload = json.dumps(payload, default=str)
        payload = json.loads(payload)
    finally:
        deserialized_model = obj_type()
        for field in deserialized_model.__fields:
            sub_obj_name = getattr(obj_type, field).obj_name

            if sub_obj_name in payload:
                setattr(deserialized_model,
                        field,
                        __deserialize(getattr(obj_type, field), payload[sub_obj_name]))

        return deserialized_model


def __deserialize(attribute, payload):
    if payload is None:
        return None

    if attribute.obj_type in PRIMITIVE_TYPES:
        return __deserialize_primitive(attribute, payload)
    elif attribute.obj_type in MAPPING_TYPES:
        return __deserialize_mapping(attribute, payload)
    elif attribute.obj_type in SEQUENCE_TYPES:
        return __deserialize_sequence(attribute, payload)
    elif attribute.obj_type in DATETIME_TYPES:
        return __deserialize_datetime(attribute, payload)
    elif issubclass(attribute.obj_type, Model):
        return __deserialize_model(attribute, payload)
    else:
        raise DeserializationException(
            f"__deserialize couldn't parse {attribute.obj_type}({payload})")


def __deserialize_primitive(attribute, payload):
    try:
        return attribute.obj_type(payload)
    except (TypeError, ValueError) as e:
        raise DeserializationException(
            f"__deserialize_primitive couldn't parse {attribute.obj_type}({payload})") from e


def __deserialize_sequence(attribute, payload):
    deserialized_list = [__deserialize(
        attribute.nested_type, obj) for obj in payload]
    return deserialized_list


def __deserialize_mapping(attribute, payload):
    return {k: __deserialize(v, attribute.nested_type)
            for k, v in payload.items()}


def __deserialize_datetime(attribute, payload):
    parsed_datetime = parse(payload)
    if attribute.obj_type is date:
        return parsed_datetime.date()
    else:
        return parsed_datetime


def __deserialize_model(attribute, payload):
    deserialized_model = attribute.obj_type()

    for field in attribute.obj_type.__fields:
        sub_obj_name = getattr(attribute.obj_type, field).obj_name

        if sub_obj_name in payload:
            setattr(deserialized_model,
                    field,
                    __deserialize(getattr(attribute.obj_type, field), payload[sub_obj_name]))

    return deserialized_model
