
from foundations_spec import *
from foundations_contrib.config.bucket_type_fetcher import for_scheme

class TestBucketTypeFetcher(Spec):
    
    def test_for_scheme_returns_default_when_none_specified(self):     
        default_bucket = Mock()
        bucket_type = for_scheme(scheme=None, default=default_bucket)
        self.assertEqual(default_bucket, bucket_type)
    
    def test_for_scheme_returns_local_filesystem_bucket_when_scheme_local(self):
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        bucket_type = for_scheme(scheme='local', default=None)
        self.assertEqual(LocalFileSystemBucket, bucket_type)
    
    def test_for_scheme_returns_error_when_scheme_not_recognized(self):
        with self.assertRaises(ValueError) as error_context:
            bucket_type = for_scheme(scheme='lou', default=None)
        
        error_message = 'Invalid uri scheme `lou` supplied - supported schemes are: local'
        self.assertIn(error_message, error_context.exception.args)
    
    def test_for_scheme_returns_error_when_scheme_not_recognized_different_scheme(self):
        with self.assertRaises(ValueError) as error_context:
            bucket_type = for_scheme(scheme='hana', default=None)
        
        error_message = 'Invalid uri scheme `hana` supplied - supported schemes are: local'
        self.assertIn(error_message, error_context.exception.args)