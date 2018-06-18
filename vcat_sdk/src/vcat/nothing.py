class Nothing(object):

    def map(self, function):
        return Nothing()

    def is_present(self):
        return False

    def get(self):
        raise ValueError('Tried #get on Nothing')

    def get_or_else(self, value):
        return value

    def fallback(self, callback):
        from vcat.option import Option
        return Option(callback())
