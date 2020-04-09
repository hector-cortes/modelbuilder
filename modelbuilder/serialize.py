from datetime import date, datetime
from functools import singledispatch

from model import Attribute


@singledispatch
def serialize(obj):
    obj_dict = {}
    for field in obj.__fields:
        if getattr(obj, field):
            obj_dict.update(
                {getattr(type(obj), field).obj_name: serialize(getattr(obj, field))})
    return obj_dict


@serialize.register(dict)
def _(obj):
    return obj


@serialize.register(list)
def _(obj):
    return [serialize(sub_obj) for sub_obj in obj]


@serialize.register(tuple)
def _(obj):
    return (serialize(sub_obj) for sub_obj in obj)


@serialize.register(int)
@serialize.register(str)
@serialize.register(bool)
def _(obj):
    return obj


@serialize.register(date)
@serialize.register(datetime)
def _(obj):
    return obj.isoformat()
