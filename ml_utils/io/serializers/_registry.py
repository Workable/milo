from collections import OrderedDict

__serializers_registry = OrderedDict()


class UnknownObjectType(KeyError):
    """
    Exception raised when unknown object is asked to be serialized.
    """
    pass


class UnknownSerializer(KeyError):
    """
    Exception raised when an unknown serialized was asked to be used.
    """
    pass


def find_suitable_serializer(obj):
    """
    Find serializer that is suitable for this operation
    :param T obj: The object that needs to be serialized
    :return: The first suitable serializer for this type of object
    :rtype: ml_utils.io.serializers.SerializerBase
    """

    for serializer in __serializers_registry.values():
        if serializer.can_process(obj):
            return serializer

    raise UnknownObjectType("Cannot find a suitalble serializer for object of type {}".format(type(object)))


def get_serializer_by_id(serializer_id):
    """
    Find a serialized based on its id
    :rtype: str serializer_id: The id of the serializer as it was provided by Serializer.serializer_id()
    :return: The serializer
    :rtype: ml_utils.io.serializers.SerializerBase
    """
    if serializer_id in __serializers_registry:
        return __serializers_registry[serializer_id]

    raise UnknownSerializer("Unknown serializer with id: {}".format(serializer_id))


def register_serializer(serializer):
    """
    Register a serializer in registry
    :param ml_utils.io.serializers.SerializerBase serializer:
    :return: The serializer itself, so that it can be used as class decorator function
    """

    global __serializers_registry
    __serializers_registry[serializer.serializer_id()] = serializer
    return serializer