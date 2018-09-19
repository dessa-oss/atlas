"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class PropertyModel(object):
    """Convenience class for automatically assigning values to named
    properties from a constructor.
    """

    def __init__(self, **kwargs):
        for property_name, model_property in self._properties():
            model_property.fset(self, kwargs.get(property_name))

    @staticmethod
    def define_property():
        """Defines an attribute on a model automatically and creates properties for it
        
        Returns:
            property -- The property defined
        """


        import random
        attribute_name = '_%08x' % random.getrandbits(32)

        def getter(self):
            return getattr(self, attribute_name)

        def setter(self, value):
            setattr(self, attribute_name, value)

        return property(getter, setter)

    @property
    def attributes(self):
        attributes = {}

        for property_name, model_property in self._properties():
            attributes[property_name] = model_property.fget(self)
        
        return attributes

    def _properties(self):
        for property_name, model_property in self.__class__.__dict__.items():
            if isinstance(model_property, property):
                yield property_name, model_property

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.attributes == other.attributes

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.attributes.__str__()

    def __repr__(self):
        return self.attributes.__repr__()