import unittest
from flask import Flask
from flask_testing import TestCase

class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config.from_object('config_test')
        return app

    def test_test(self):
      self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
