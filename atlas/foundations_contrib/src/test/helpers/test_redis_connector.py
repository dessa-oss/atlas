
import unittest
from mock import Mock


class TestRedisConnector(unittest.TestCase):

    def setUp(self):
        from foundations_contrib.helpers.redis_connector import RedisConnector
        from foundations_contrib.config_manager import ConfigManager

        self._config_manager = ConfigManager()
        self._connection_callback = Mock()
        self._connection = Mock()
        self._connection_callback.return_value = self._connection
        self._environment = {}
        self._connector = RedisConnector(
            self._config_manager, self._connection_callback, self._environment)

    def test_call_calls_callback_with_connection_string_missing(self):
        self._connector()
        self._connection_callback.assert_called_once_with(
            'redis://:@localhost:6379')

    def test_call_returns_result_of_callback(self):
        result = self._connector()
        self.assertEqual(self._connection, result)

    def test_call_calls_callback_with_connection_string(self):
        self._config_manager['redis_url'] = 'redis://lou:7733'
        self._connector()
        self._connection_callback.assert_called_once_with('redis://:@lou:7733')

    def test_call_calls_callback_with_connection_string_different_connection(self):
        self._config_manager['redis_url'] = 'redis://feifei:9733'
        self._connector()
        self._connection_callback.assert_called_once_with(
            'redis://:@feifei:9733')

    def test_call_returns_result_of_callback_with_connection_string(self):
        self._config_manager['redis_url'] = 'redis://feifei:9733'
        result = self._connector()
        self.assertEqual(self._connection, result)

    def test_call_raises_exception_when_a_connection_error_happens(self):
        self._connection.ping.side_effect = self._raise_connection_error
        with self.assertRaises(ConnectionError) as error_context:
            self._connector()
        self.assertIn('Unable to connect to Redis, due to potential encryption error.', error_context.exception.args)

    def test_call_raises_exception_underlying_exception(self):
        self._connection.ping.side_effect = self._raise_configuration_error
        with self.assertRaises(ValueError) as error_context:
            self._connector()
        self.assertIn('Invalid connection.', error_context.exception.args)

    def test_call_raises_exception_when_an_unexpected_error_happens(self):
        import redis

        self._connection.ping.side_effect = self._raise_different_connection_error
        with self.assertRaises(redis.exceptions.ConnectionError) as error_context:
            self._connector()
        self.assertIn('Something broke!', error_context.exception.args)

    def _raise_connection_error(self):
        import redis

        raise redis.exceptions.ConnectionError(redis.connection.SERVER_CLOSED_CONNECTION_ERROR)

    def _raise_different_connection_error(self):
        import redis

        raise redis.exceptions.ConnectionError('Something broke!')

    def _raise_configuration_error(self):
        raise ValueError('Invalid connection.')

    def test_call_calls_callback_with_unix_connection_string_without_password(self):
        self._config_manager['redis_url'] = 'unix:///var/run/redis.sock?db=0'
        self._connector()
        self._connection_callback.assert_called_once_with('unix://:@/var/run/redis.sock?db=0')
