import json
import unittest

from app.models import Call, Duration
from app.call_duration_queue import CallDurationQueue


class CallDurationQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = CallDurationQueue()

        # Male call from fixtures
        with open("tests/fixtures/call/call1.json", 'r') as f:
            json_data = json.load(f)
            self.call = Call(**json_data)

        # Male call from fixtures
        with open("tests/fixtures/duration/duration1.json", 'r') as f:
            json_data = json.load(f)
            self.duration = Duration(**json_data)

    def test_init_obj_True(self):
        self.assertIsInstance(self.queue, CallDurationQueue)

    def test_init_obj_False(self):
        with self.assertRaisesRegex(
                TypeError,
                "takes 1 positional argument but 2 were given"):
            CallDurationQueue("Hello world!")

    def test_init_True(self):
        self.assertIsInstance(self.queue.calls, list)
        self.assertIsInstance(self.queue.duration, list)
        self.assertFalse(self.queue.calls)
        self.assertFalse(self.queue.duration)

    def test_add_object_call_True(self):
        self.queue.add_object(self.call)
        self.assertEquals(self.queue.calls[0], self.call)
        del self.queue.calls[0]

    def test_add_object_call__result(self):
        """Check that no result when we just add one call"""
        result = self.queue.add_object(self.call)
        self.assertFalse(result)
        del self.queue.calls[0]

    def test_add_object_duration_True(self):
        self.queue.add_object(self.duration)
        self.assertEquals(self.queue.duration[0], self.duration)
        del self.queue.duration[0]

    def test_add_object_duration_result(self):
        """Check that no result when we just add one duration"""
        result = self.queue.add_object(self.duration)
        self.assertFalse(result)
        del self.queue.duration[0]

    def test_add_object_call_and_duration_result(self):
        self.queue.add_object(self.call)
        result = self.queue.add_object(self.duration)

        # Check that queue is empty now
        self.assertFalse(self.queue.calls)
        self.assertFalse(self.queue.duration)

        # And get correct result
        self.assertDictEqual(result, {'matched': {
            'duration': self.duration, 'call': self.call}
        })

if __name__ == '__main__':
 unittest.main()