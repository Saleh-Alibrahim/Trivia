import os
import unittest
import json
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://Saleh:123@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)
        self.new_question = {
            "answer": "3600",
            "category": "1",
            "difficulty": 3,
            "question": "How many seconds in 1 hour ?"
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


def test_retrieve_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['questions'])
    self.assertEqual(data['total_questions'])
    self.assertEqual(data['categories'])
    self.assertEqual(data['current_category'])


def test_retrieve_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['categories'])


def test_delete_question(self):
    res = self.client().delete('/questions/37')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['questions'])
    self.assertEqual(data['total_questions'])
    self.assertEqual(data['categories'])
    self.assertEqual(data['current_category'])


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
    self.assertEqual(data['questions'])
    self.assertEqual(data['total_questions'])
    self.assertEqual(data['categories'])
    self.assertEqual(data['current_category'])


def test_get_questionByCategory(self):
    res = self.client().get('/categories/1/questions')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['questions'])


def test_404_get_questionByCategory(self):
    res = self.client().get('/categories/1000/questions')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')


def test_play_quiz(self):
    res = self.client().post(
        '/quizzes', json={'previous_questions': [], 'quiz_category': 1})
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
