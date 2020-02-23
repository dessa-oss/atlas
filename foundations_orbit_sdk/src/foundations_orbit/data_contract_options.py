

class DataContractOptions(object):
    
    def __init__(self, check_row_count=None, check_special_values=None, check_distribution=None, check_min_max=None, check_domain=None, check_uniqueness=None):
        self.check_row_count = check_row_count
        self.check_special_values = check_special_values
        self.check_distribution = check_distribution
        self.check_min_max = check_min_max
        self.check_domain = check_domain
        self.check_uniqueness = check_uniqueness

    def __eq__(self, other):
        return isinstance(other, DataContractOptions) \
            and self._other_attributes_equal(other)

    def _other_attributes_equal(self, other):
        return self.check_row_count == other.check_row_count \
            and self.check_special_values == other.check_special_values \
            and self.check_distribution == other.check_distribution \
            and self.check_min_max == other.check_min_max \
            and self.check_domain == other.check_domain \
            and self.check_uniqueness == other.check_uniqueness


def _equality_check(value, other_value):
    import math

    if math.isnan(value):
        return math.isnan(other_value)

    return value == other_value

def _zipped_elements_equal(values, other_values):
    for value, other_value in zip(values, other_values):
        if not _equality_check(value, other_value):
            return False

    return True