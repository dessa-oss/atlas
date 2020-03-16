
from foundations_spec import *

class TestSaveArtifact(Spec):

    def test_save_artifact_is_available_from_foundations(self):
        import foundations
        from foundations_contrib.archiving.save_artifact import save_artifact

        self.assertEqual(save_artifact, foundations.save_artifact)