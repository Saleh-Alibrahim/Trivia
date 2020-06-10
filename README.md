# Full Stack Trivia API Project
This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python main.py
```

## Testing
To run the tests, run
```
python test_flaskr.py
```
Omit the dropdb command the first time you run tests.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return four types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 500 – unprocessable

### Endpoints

#### GET /categories

* General: Returns a list categories.
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
        "categories": [
            "sport",
             "fear",
             "good"
            ]
        }


#### GET /questions

* General:
  * Returns a list questions.
  * Results are paginated in groups of 10.
  * Also returns list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions`<br>

        {
         "categories": [
            "sport",
            "fear",
            "good"
        ],
        "current_category": "current_categorysList",
        "questions": [
            {
            "answer": "Lorem ipsum dolor sit amet",
            "category": "1",
            "difficulty": 1,
            "id": 1,
            "question": "Lorem ipsum dolor sit amet"
            },
            {
            "answer": "consectetur adipiscing elit. Morbi tincidunt ",
            "category": "2",
            "difficulty": 1,
            "id": 2,
            "question": "consectetur adipiscing elit. Morbi tincidunt "
            },
            {
            "answer": "risus placerat tempus dictum. Ut tellus ex,",
            "category": "3",
            "difficulty": 3,
            "id": 3,
            "question": "risus placerat tempus dictum. Ut tellus ex,"
            },
            {
            "answer": "Lorem ipsum dolor sit amet, consectetur",
            "category": "1",
            "difficulty": 1,
            "id": 4,
            "question": "Lorem ipsum dolor sit amet, consectetur"
            }
        ],
        "total_questions": 4
        }

#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question by id using url parameters.
  * Returns list of  questions with out the deleted question.
* Sample: `curl http://127.0.0.1:5000/questions/1 -X DELETE`<br>

       
            {
            "answer": "consectetur adipiscing elit. Morbi tincidunt ",
            "category": "2",
            "difficulty": 1,
            "id": 2,
            "question": "consectetur adipiscing elit. Morbi tincidunt "
            },
            {
            "answer": "risus placerat tempus dictum. Ut tellus ex,",
            "category": "3",
            "difficulty": 3,
            "id": 3,
            "question": "risus placerat tempus dictum. Ut tellus ex,"
            },
            {
            "answer": "Lorem ipsum dolor sit amet, consectetur",
            "category": "1",
            "difficulty": 1,
            "id": 4,
            "question": "Lorem ipsum dolor sit amet, consectetur"
            }

#### POST /questions

This endpoint either creates a new question or returns search results.

1. If no search term is included in request:

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question, as well as paginated questions.
  * Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json"'`  
  * body <br>

         {
         "answer": "Devworks is a full stack JavaScript Bootcamp located in the heart",
        "category": "sport",
         "difficulty": 3,
        "question": "Lorem "
         }

  * Result : <br> 

             {
            "answer": "consectetur adipiscing elit. Morbi tincidunt ",
            "category": "2",
            "difficulty": 1,
            "id": 2,
            "question": "consectetur adipiscing elit. Morbi tincidunt "
            },
            {
            "answer": "risus placerat tempus dictum. Ut tellus ex,",
            "category": "3",
            "difficulty": 3,
            "id": 3,
            "question": "risus placerat tempus dictum. Ut tellus ex,"
            },
            {
            "answer": "Lorem ipsum dolor sit amet, consectetur",
            "category": "1",
            "difficulty": 1,
            "id": 4,
            "question": "Lorem ipsum dolor sit amet, consectetur"
            },
            {
            "answer": "Devworks is a full stack JavaScript Bootcamp located in the heart",
             "category": "1",
            "difficulty": 3,
            "id": 5,
            "question": "Lorem "
            }
        



2. If search term <strong>is</strong> included in request:

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with  matching questions.
* Sample: `curl http://127.0.0.1:5000/questions/lorem -X POST -H "Content-Type: application/json"'`<br>

 * Will return every question include the word lorem.
 

#### GET /categories/\<int:id\>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/categories/3/questions`<br>

        {
            "questions": [
            {
            "answer": "risus placerat tempus dictum. Ut tellus ex,",
            "category": "3",
            "difficulty": 3,
            "id": 3,
            "question": "risus placerat tempus dictum. Ut tellus ex,"
            }
            ]
            "success": true
        }

#### POST /quizzes

* General:
  * Allows users to play the quiz game.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question not among previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" `
* body <br>

        {
            "previous_questions": [3, 4],
            "quiz_category": {"type": "sport", "id": "1"}
        }
* Result <br>

        {
            "question": {
               "answer": "risus placerat tempus dictum. Ut tellus ex,",
                "category": "3",
                "difficulty": 3,
                "id": 3,
                "question": "risus placerat tempus dictum. Ut tellus ex,"
            }
            }, 
            "success": true
        }

## Authors

Saleh Alibrahim authored the API (`main.py`), test suite (`test_flaskr.py`), and this README.<br>
All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/) as a project template for the [Full Stack Web Developer Nanodegree]