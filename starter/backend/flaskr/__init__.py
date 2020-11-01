import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_api import status
import json
import random
from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={'/': {"origins": "*"}})

  @app.route('/')
  def hello():
   return 'Hello world'
 

  
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,PATCH,POST,DELETE,OPTIONS')
    return response




  def getQuestionsService(page):
      try:
        return Question.query.order_by(
            Question.id.desc()
        ).paginate(page, per_page=QUESTIONS_PER_PAGE)

      except OperationalError as e:
           print("Operational exception: "+ e)
           abort(404)

        

  def getCatagoriesService():
   categories =   Category.query.all()
   categories_type = {}
   for category in categories:
     categories_type[category.id] = category.type

   if len(categories_type) == 0:
            abort(404)

   return jsonify({
    'success': True,
    'categories': categories_type,
    'total_categories': len(categories)
    })



  def createCatagoryService(type):
       catagory = Category(type= type)
       db.session.add(catagory)
       db.session.commit()
       return 'new catagory is created'
 


  def createQuestionsService(question,answer,catagory,difficulty):
    try:
        question = Question(
                    question=question,
                    answer=answer,
                    category=catagory,
                    difficulty=difficulty)

        db.session.add(question)
        db.session.commit()
        print("Question was successfully created")
    except Exception as e:
        print("Exception occured:  "+ e)
        db.session.rollback()
    finally:
        db.session.close()


  @app.route('/categories')
  def getAllCatagories():
   return getCatagoriesService(), status.HTTP_200_OK
 


  @app.route('/categories', methods=['POST'])
  def createCatagory():
   content =  request.get_json()
   type = content.get('type', None)
   return createCatagoryService(type), status.HTTP_201_CREATED



  @app.route('/questions')
  @app.route('/questions/page/<int:page>')
  def getQuestions(page=1):
    return getQuestionsService(page), status.HTTP_200_OK

  @app.route('/questions', methods=['POST'])
  def createQuestions():
    content =  request.get_json()
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    return createQuestionsService(question,answer,catagory,difficulty), status.HTTP_201_CREATED






  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(500)
  def server_error(error):
    return 'System error', 500

  return app






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

'''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

'''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

'''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

'''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

'''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
'''


