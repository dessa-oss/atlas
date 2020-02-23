
from foundations_spec import *

@quarantine
class TestClassStageDeployment(Spec):
    
    class TestClass(object):
        def __init__(self):
            pass

    def test_can_create_stage_with_class(self):
        import foundations

        test_stage = foundations.create_stage(self.TestClass)()
        test_stage.run()
