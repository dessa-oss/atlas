from time import sleep
import sys
import foundations

t = int(sys.argv[1])

sleep(t)
print(sys.argv[2])
print(foundations.__version__)

try:
    x = sys.argv[3]
except IndexError:
    raise
