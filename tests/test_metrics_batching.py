import threading
import time
import unittest
from unittest.mock import MagicMock, patch
from idm_logger.metrics import MetricsWriter

class TestMetricsBatching(unittest.TestCase):
    def setUp(self):
        # Prevent MetricsWriter from starting the worker thread immediately
        # or mock the session before it starts using it.
        pass

    @patch('requests.Session')
    def test_batching(self, mock_session_cls):
        # Create a mock session
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.post.return_value.status_code = 200

        # Initialize MetricsWriter
        writer = MetricsWriter()

        # Add 3 items to the queue rapidly
        writer.write({"temp": 1})
        writer.write({"temp": 2})
        writer.write({"temp": 3})

        # Wait for the worker to process (timeout is 1s, so 2s is safe)
        time.sleep(2.0)

        # Stop the writer
        writer.stop()

        # Verify call count
        print(f"\nNumber of calls to session.post: {mock_session.post.call_count}")

        # Inspect what was sent
        for i, call in enumerate(mock_session.post.call_args_list):
            print(f"Call {i+1} data: {call[1]['data']}")

        # We expect 1 call because the items were added rapidly and timeout is 1s
        self.assertEqual(mock_session.post.call_count, 1, "Expected 1 call with batching")

        # Verify payload contains all 3 measurements separated by newlines
        call_args = mock_session.post.call_args
        self.assertIsNotNone(call_args)
        data = call_args[1]['data']
        expected_lines = [
            "idm_heatpump temp=1",
            "idm_heatpump temp=2",
            "idm_heatpump temp=3"
        ]
        actual_lines = data.split('\n')
        self.assertEqual(len(actual_lines), 3)
        self.assertEqual(actual_lines, expected_lines)

    @patch('requests.Session')
    def test_batching_flush_on_stop(self, mock_session_cls):
        # Test that remaining items are flushed on stop
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.post.return_value.status_code = 200

        writer = MetricsWriter()
        writer.write({"temp": 99})

        # Stop immediately, before timeout
        writer.stop()

        self.assertEqual(mock_session.post.call_count, 1, "Expected flush on stop")
        data = mock_session.post.call_args[1]['data']
        self.assertEqual(data, "idm_heatpump temp=99")

if __name__ == '__main__':
    unittest.main()
