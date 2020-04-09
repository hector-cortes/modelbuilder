class SerializationException(Exception):
    """Exceptions raised during response serialization"""


class DeserializationException(Exception):
    """Exceptions raised during request deserialization"""


class RequiredAttributeException(Exception):
    """Exceptions raised when an attribute marked as required is deleted"""
