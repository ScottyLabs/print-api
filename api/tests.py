# Simple unittests
import unittest
import api.printfile

class PrintfileTest(unittest.TestCase):
    # Implement request as empty class for now
    def setUp(self):
        class FakeRequest(object):
            def __init__(self):
                self.form = dict()

        self.request = FakeRequest()


    def test_has_andrew_id(self):
        ANDREW_ID_KEY = "andrew_id"

        good_ids = ("jdoe", "abcd1")
        bad_ids = ("h i", "hello@")

        for good_id in good_ids:
            self.request.form[ANDREW_ID_KEY] = good_id
            self.assertTrue(api.printfile.has_andrew_id(self.request))

        for bad_id in bad_ids:
            self.request.form[ANDREW_ID_KEY] = bad_id
            self.assertFalse(api.printfile.has_andrew_id(self.request))


if __name__ == "__main__":
    unittest.main(verbosity=2)

