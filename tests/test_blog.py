import os
import tempfile
import pytest
import unittest
import flask
from flask import jsonify
from app import app
import json, os, re
from calendarfunc import *
from prof import *



class BlogTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 
        return app

    def test_home_get(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_home_post(self):
        data = [['Event1','2021-01-01 00:00:00','2021-01-01 00:00:01'],['Event2','2021-01-01 00:00:00','2021-01-01 00:00:02']]
        data = json.dumps(data)
        response = self.app.post('/', data = data, content_type='application/json')
        assert response.status_code == 200

    def test_professor_get(self):
        prof = "/professor?prof=Ashish%20Choudhury"
        response = self.app.get('/professor', data = prof, content_type='application/text')
        assert response.status_code == 200

    # def test_ajax_post(self):
    #     data = {}
    #     data["query"] = 'DS101'
    #     response = self.app.post('/ajax/', data = data, content_type='application/text')
    #     assert response.status_code == 200






if __name__ == '__main__':
  unittest.main()