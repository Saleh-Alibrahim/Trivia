import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add("Access-Control-Allow-Headers",
                         "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")

    return response


@app.route('/categories')
def retrieve_categories():
    try:
        categorysList = Category.query.order_by(Category.id).all()
        result = []
        for category in categorysList:
            result.append(category.format())
        return jsonify({
            'categories': result
        })
    except:
        abort(500)


@app.route('/questions')
def retrieve_questions():
    try:
        questionsList = Question.query.order_by(Question.id).all()
        categorysList = Category.query.order_by(Category.id).all()

        current_questions = paginate_questions(request, questionsList)
        result = []
        for category in categorysList:
            result.append(category.format())
        return jsonify({
            'questions': current_questions,
            'total_questions': len(questionsList),
            'categories': result,
            'current_category': " ",
        })
    except:
        abort(500)


@ app.route('/questions/<int:question_id>', methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()
    if question is None:
        abort(404)
    try:
        question.delete()
        questions = retrieve_questions()
        return questions
    except:
        abort(405)


@app.route('/questions', methods=["POST"])
def create_question():
    try:

        body = request.get_json()
        if body is None:
            abort(422)
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', 'no category')
        new_difficulty = body.get('difficulty', None)
        question = Question(question=new_question, answer=new_answer,
                            category=new_category, difficulty=new_difficulty)
        question.insert()
        questions = retrieve_questions()
        return questions
    except:
        abort(422)


@ app.route('/questions/<string:word>', methods=["POST"])
def get_questionByWord(word):
    try:
        tag = f"%{word}%"
        questionsList = Question.query.order_by(Question.id).filter(
            Question.question.ilike(tag)).all()
        current_questions = paginate_questions(request, questionsList)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions)
        })
    except:
        abort(404)


@app.route('/categories/<int:id>/questions', methods=["GET"])
def get_questionByCategory(id):
    try:
        id += 1
        id = 1
        questionsList = Question.query.filter(
            Question.category == str(id)).all()
        current_questions = paginate_questions(request, questionsList)
        return jsonify({
            'success': True,
            'questions': current_questions
        })
    except:
        abort(400)


@app.route('/quizzes', methods=["POST"])
def play_quiz():
    try:

        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        question = ''
        if str(quiz_category['type']) == 'click':
            question = Question.query.filter(
                Question.id.notin_(previous_questions)).first()
        else:
            id = int(quiz_category['id']) + 1
            question = Question.query.filter(
                Question.id.notin_(previous_questions)).filter(Question.category == str(id)).first()

        if question is not None:
            question = question.format()
        return jsonify({
            'success': True,
            'question': question
        })
    except:
        abort(400)


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500


if __name__ == '__main__':
    app.debug = True
    app.run()
