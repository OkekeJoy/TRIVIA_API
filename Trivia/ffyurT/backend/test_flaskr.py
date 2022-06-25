import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "break", "localhost:5432", self.database_name
)
        setup_db(self.app, self.database_path)
        self.new_question= {'question': 'what is the largest river in Nigeria',
        'amswer': 'River Niger', 'difficulty': '100', 'category': 'Science'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass
    

    def test_get_paginated_questions(self):
        res= self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)

            
    def test_get_available_category(self):
        res= self.client().get('/categories')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category(self):
        res= self.client().get('/categories/<int:category_id>/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_delete_question_by_id(self):
        res=self.client().delete('/questions/<int:question_id>')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_post_newquetion(self):
        res=self.client().post('/questions', json=self.new_question)
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()