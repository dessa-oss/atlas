from vcat import ResultReader, GCPFetcher

def main():
  reader = ResultReader(GCPFetcher())
  print(reader.as_dict())

if __name__ == "__main__":
  main()