from vcat import *
from pandas import DataFrame


def create_data_frame():
    return DataFrame([[0]], columns=["hello"])

def print_it(thing):
  print(thing)
  return thing

data_frame = pipeline | create_data_frame
something = data_frame["hello"].count() | print_it
thing = data_frame["world"] = [99999]
print(thing)
something.run()
