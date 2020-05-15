import os
import tempfile
import pytest
import unittest
import flask
import app

class BlogTestCase(unittest.TestCase):

    def setUp(self):
    #    # self.app = flaskr.blog.test_client()
    #     self.app.testing = True 
    #     return app
        pass

    def test_home(self):
        # self.flaskr.blog.get('/')
        # self.assert_template_used('home.html')
        pass

if __name__ == '__main__':
  unittest.main()