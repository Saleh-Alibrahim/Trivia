import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from models import setup_db, Question, Category
from main import app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.client = app.test_client
        setup_db(
            app, f'postgresql://Saleh:123@localhost:5432/trivia_test')
        self.new_question = {
            "answer": "3600",
            "category": "1",
            "difficulty": 3,
            "question": "How many seconds in 1 hour ?"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 5)

    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_questionByCategory(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
