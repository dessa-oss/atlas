def print_it(self):
  print(self)
  return self, {'self': self}

def destroy_it(self):
  raise RuntimeError(self)