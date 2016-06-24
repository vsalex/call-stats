import unittest
import json

from app.models import DailyStatObj, Call, Duration


class DailyStatTestCase(unittest.TestCase):
    def setUp(self):
        self.dso = DailyStatObj()

    def test_init_obj_True(self):
        self.assertIsInstance(self.dso, DailyStatObj)

    def test_init_obj_False(self):
        with self.assertRaisesRegex(
                TypeError,
                "takes 1 positional argument but 2 were given"):
            DailyStatObj("Hello world!")

    def test_init_True(self):
        self.assertIsInstance(self.dso.errors, list)
        self.assertIs(self.dso.entry_time, None)

    def test_set_call_id_true(self):
        call_id = 1155
        self.dso._set_call_id(call_id, int)
        self.assertEqual(call_id, self.dso.call_id)

    def test_set_call_id_false(self):
        call_id = 1155
        self.dso._set_call_id(call_id, str)
        self.assertEqual(False, self.dso.call_id)


class CallTestCase(unittest.TestCase):
    def setUp(self):
        # Load data from fixtures
        with open("tests/fixtures/call/call1.json", 'r') as f:
            json_data = json.load(f)
            for k,v in json_data.items():
                setattr(self, k, v)

    def test_init_obj_True(self):
        self.call = Call(self.call_id, self.timestamp, self.source_number,
                         self.dest_number)
        self.assertIsInstance(self.call, Call)

    def test_init_obj_False(self):
        with self.assertRaisesRegex(
                TypeError,
                "missing 4 required positional arguments: 'call_id', "
                "'timestamp', 'source_number', and 'dest_number'"):
            self.call = Call()


class DurationTestCase(unittest.TestCase):
    def setUp(self):
        self.call_id = "call_id"
        self.duration = 22

    def test_init_obj_True(self):
        self.duration = Duration(self.call_id, self.duration)
        self.assertIsInstance(self.duration, Duration)

    def test_init_obj_False(self):
        with self.assertRaisesRegex(
                TypeError,
                "missing 2 required positional arguments: 'call_id' and "
                "'duration'"):
            self.duration = Duration()

if __name__ == '__main__':
    unittest.main()