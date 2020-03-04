with open("licenses.tgz", "rb") as f:
    b = f.read()
    print(int.from_bytes(b, byteorder='little', signed=True), len(b))
