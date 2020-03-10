import sys

tar_file = sys.argv[1]


with open(tar_file, "rb") as f:
    b = f.read()
    print(int.from_bytes(b, byteorder='little', signed=True), len(b))
