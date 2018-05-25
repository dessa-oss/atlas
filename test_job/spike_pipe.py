def print_it(self):
  print(self)
  return self

def destroy_it(self):
  raise RuntimeError(self)