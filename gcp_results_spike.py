from vcat import *

def main():
  reader = ResultReader(GCPBundleFetcher())
  print(reader.as_dict())

if __name__ == "__main__":
  main()