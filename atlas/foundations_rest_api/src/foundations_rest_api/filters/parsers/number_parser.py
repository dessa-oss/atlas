

class NumberParser(object):

    def parse(self, value):
        try:
            return float(value)
        except TypeError:
            raise ValueError('Not able to convert "{}" to a number'.format(str(value)))
