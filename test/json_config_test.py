import json
import unittest2

class TestJsonMethods(unittest2.TestCase):

    def test_json(self):
        with open('../config.json') as json_file:
            
            data = json.load(json_file)
            self.assertTrue(len(str(data["database"]["host"])) > 0)
            self.assertTrue(len(str(data["database"]["port"]))> 0)
            self.assertTrue(len(str(data["database"]["user"]))> 0)
            self.assertTrue(len(str(data["database"]["passwd"]))> 0)
            self.assertTrue(len(str(data["database"]["db"]))> 0)

if __name__ == '__main__':
    unittest2.main()
