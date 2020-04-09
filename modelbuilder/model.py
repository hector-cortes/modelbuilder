import json

from inspect import Signature, Parameter
from weakref import WeakKeyDictionary
from datetime import date, datetime


class Attribute:
    """ A class that implements a descriptor protocol.

        https://docs.python.org/3.8/howto/descriptor.html
    """
    PRIMITIVES = set((bool, str, int, float, bytes, datetime, date))
    SEQUENCES = set((list, tuple))
    MAPPINGS = [dict]

    def __init__(self, obj_name, obj_type, nested_type=None):
        """ Creates a new instance of Attribute.

        Definitions:
            Managed Class:
                The class where Attribute instances are declared as class attributes.
                Managed classes should always inherit from Model()
            Managed Instance:
                An instance of the Managed Class
            Descriptor Instances:
                Each instance of Attribute(), declared as a class attribute of a Managed Class
        Args:
            name: The attribute name used by Managed Classes
            values: A WeakKeyDictionary that maps Managed Instances to instance-specific values
            obj_name: The name used as the JSON key, when deserializing the Managed Class into a JSON style object
            obj_type: The object type that Descriptor Instnaces can be set to
            nested_type: If obj_type is a list, tuple, or dict then nested_type specifies the allowed sub-item type
        Raises:
            TypeError: The Descriptor Instance was assigned a value whose type != self.obj_type
            TypeError: The Descriptor Instance was assigned an invalid value for self.nested_type
        """
        self.values = WeakKeyDictionary()
        self.obj_name = obj_name
        self.obj_type = obj_type
        self.nested_type = NestedType(nested_type)

    def __get__(self, instance, owner):
        if instance:
            return self.values.get(instance, None)
        else:
            return self

    def __set__(self, instance, value):
        if self.obj_type in self.SEQUENCES:
            for obj in value:
                if not isinstance(obj, self.nested_type.obj_type):
                    raise TypeError(
                        f'{obj} is a {type(obj)}, and is not included in {self.name}.nested_type: {self.nested_type.obj_type}')
        elif self.obj_type in self.MAPPINGS:
            for dict_value in value.values():
                if not isinstance(dict_value, self.nested_type.obj_type):
                    raise TypeError(
                        f'{dict_value} is a {type(dict_value)}, and is not included in {self.name}.nested_type: {self.nested_type.obj_type}')
        elif self.obj_type in self.PRIMITIVES:
            if not isinstance(value, self.obj_type):
                raise TypeError(
                    f'{type(instance)}.{self.name} can only be set to {self.obj_type}; Was given a {type(value)}')
        elif not issubclass(type(value), Model):
            raise TypeError(
                f'{type(value)} is invalid type for {type(instance)}.{self.name}')

        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]

    def __set_name__(self, owner, name):
        self.name = name

    def __repr__(self):
        return f"Attribute(obj_name={self.obj_name}, obj_type={self.obj_type}, self.nested_type={self.nested_type})"


class NestedType:
    """ A class meant to mimic Attribute. Its sole purpose is to create an object with an
        attribute "obj_type", which makes it nicer to pass in to the __deserialize()
        function of model_builder.deserialize
    """

    def __init__(self, nested_type):
        self.obj_type = nested_type


class __ModelMeta(type):
    """ A MetaClass used to embed the necessary hooks for model_builder.serialize
        and model_builder.deserialize to function

        Attributes:
            __fields: All class attributes of type Attribute() get put into this list. It's
                      used by serialize and deserialize to dtermine which attributes should 
                      be treated as part of the Model
    """
    def __new__(cls, name, bases, body):
        fields = [key for key, value in body.items()
                  if isinstance(value, Attribute)]
        params = [Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD, default=None)
                  for name in fields]
        signature = Signature(params)

        def __init__(self, *args, **kwargs):
            bound = self.__signature__.bind(*args, **kwargs)
            for name, value in bound.arguments.items():
                setattr(self, name, value)

        def __str__(self):
            return json.dumps(self.to_dict(), indent=4)

        def to_dict(self):
            result = {}

            for field in getattr(self, '__fields'):
                if getattr(self, field):
                    obj_type = type(getattr(self, field))
                    if obj_type is list:
                        result[field] = list(map(
                            lambda x: x.to_dict() if hasattr(x, "to_dict") else
                            x, getattr(self, field)))
                    elif obj_type is dict:
                        result[field] = dict(map(
                            lambda item: (item[0], item[1].to_dict())
                            if hasattr(item[1], "to_dict") else
                            item, getattr(self, field)))
                    elif hasattr(getattr(self, field), "to_dict"):
                        result[field] = getattr(self, field).to_dict()
                    else:
                        result[field] = getattr(self, field)
            return result

        body.update({'to_dict': to_dict,
                     '__str__': __str__,
                     '__init__': __init__,
                     '__signature__': signature,
                     '__fields': fields})

        return super().__new__(cls, name, bases, body)


class Model(metaclass=__ModelMeta):
    """ Convenience class to hide the existence of ModelMeta """
