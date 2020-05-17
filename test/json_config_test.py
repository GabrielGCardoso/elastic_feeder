import json
import unittest2
import os

class TestJsonMethods(unittest2.TestCase):

    def test_json(self):
        with open(os.path.join(os.path.dirname(__file__), '../config.json')) as json_file:
            
            data = json.load(json_file)
            self.assertTrue(len(str(data["database"]["host"])) > 0)
            self.assertTrue(len(str(data["database"]["port"]))> 0)
            self.assertTrue(len(str(data["database"]["user"]))> 0)
            self.assertTrue(len(str(data["database"]["passwd"]))> 0)
            self.assertTrue(len(str(data["database"]["db"]))> 0)

if __name__ == '__main__':
    unittest2.main()
