
from foundations_spec.helpers.callback import Callback


class let(Callback):

    def assign_value(self, attribute_name, spec_instance):
        value = self.evaluate(spec_instance)
        setattr(spec_instance, attribute_name, value)
        return value