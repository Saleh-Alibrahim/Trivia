import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category


app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


'''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
'''
# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Methods",
                         "GET,HEAD,OPTIONS,POST,PUT,DELETE")
    response.headers.add("Access-Control-Allow-Headers",
                         "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")

    return response


'''
  @TODO: Use the after_request decorator to set Access-Control-Allow
'''


@ app.route('/categories')
def retrieve_categories():
    try:
        categorysList = Category.query.order_by(Category.id).all()
        result = []
        for category in categorysList:
            result.append(category.format())
        return jsonify({
            'categories': result
        })
    except Exception as error:
        print(error)
        abort(500)
        '''
      @TODO:
      Create an endpoint to handle GET requests for questions,
      including pagination (every 10 questions).
      This endpoint should return a list of questions,
      number of total questions, current category, categories.

      TEST: At this point, when you start the application
      you should see questions and categories generated,
      ten questions per page and pagination at the bottom of the screen for three pages.
      Clicking on the page numbers should update the questions.
      '''


@ app.route('/questions')
def retrieve_questions():
    try:
        questionsList = Question.query.order_by(Question.id).all()
        categorysList = Category.query.order_by(Category.id).all()

        current_questions = paginate_questions(request, questionsList)
        result = []
        for category in categorysList:
            result.append(category.format())
        print(len(questionsList))
        return jsonify({
            'questions': current_questions,
            'total_questions': len(questionsList),
            'categories': result,
            'current_category': "current_categorysList",
        })
    except Exception as error:
        print(error)
        abort(500)


@ app.route('/questions/<int:question_id>', methods=["DELETE"])
def delete_question(question_id):
    try:
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)

        question.delete()

        return redirect(url_for('retrieve_questions'))
    except Exception as error:
        print(error)
        abort(422)
    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''


@ app.route('/questions', methods=["POST"])
def create_question():
    try:
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        question = Question(question=new_question, answer=new_answer,
                            category=new_category, difficulty=new_difficulty)
        question.insert()
        return redirect(url_for('retrieve_questions'))
    except Exception as error:
        print(error)
        abort(422)
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''


@ app.route('/questions/<string:word>', methods=["POST"])
def get_questionByWord(word):
    try:
        tag = f"%{word}%"
        questionsList = Question.query.order_by(Question.id).filter(
            Question.question.like(tag)).all()
        result = []
        for question in questionsList:
            result.append(question.format())
        return jsonify({
            'success': True,
            'questions': result,
            'total_questions': len(result)
        })
    except Exception as error:
        print(error)
        abort(422)
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''


@app.route('/categories/<int:id>/questions', methods=["GET"])
def get_questionByCategory(id):
    try:
        questionsList = Question.query.order_by(Question.id).filter(
            Question.category == id).all()
        result = []
        for question in questionsList:
            result.append(question.format())
        return jsonify({
            'success': True,
            'questions': result,
            'total_questions': len(result)
        })
    except Exception as error:
        print(error)
        abort(422)

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''


# @app.route('/questions/<string:category>', methods=["GET"])
# def get_questionByCategory(category):
#     try:
#         questionsList = Question.query.order_by(Question.id).filter(
#             Question.category == category).all()
#         result = []
#         for question in questionsList:
#             result.append(question.format())
#         return jsonify({
#             'success': True,
#             'questions': result,
#             'total_questions': len(result)
#         })
#     except Exception as error:
#         print(error)
#         abort(422)
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''


if __name__ == '__main__':
    app.debug = True
    app.run()
