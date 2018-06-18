import unittest

def suite_factory():
    loader = unittest.TestLoader()
    return loader.discover(".", pattern="test*.py")

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite_factory())