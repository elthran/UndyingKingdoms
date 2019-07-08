from lib.namers import to_mixed_case


class Serializer:
    """A returns an object that is json serializable."""
    def __setattr__(self, name, value):
        """Convert Python naming to JS naming conventions."""
        self.__dict__[to_mixed_case(name)] = value

